# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class AgentMilestoneAuditor(gl.Contract):
    project_name: str
    buyer_requirements: str
    release_bps: int
    revision_bps: int
    reject_bps: int
    submission_count: int
    accepted_count: int
    disputed_count: int
    latest_submission_id: int
    latest_status: str
    latest_score: int
    latest_release_bps: int
    latest_evidence_hash: str
    latest_reason: str

    def __init__(
        self,
        project_name: str,
        buyer_requirements: str,
        release_bps: int,
        revision_bps: int,
        reject_bps: int,
    ):
        if release_bps < revision_bps or revision_bps < reject_bps:
            raise gl.vm.UserError("bps thresholds must be release >= revision >= reject")
        if reject_bps < 0 or release_bps > 10000:
            raise gl.vm.UserError("bps thresholds must be between 0 and 10000")

        self.project_name = project_name
        self.buyer_requirements = buyer_requirements
        self.release_bps = release_bps
        self.revision_bps = revision_bps
        self.reject_bps = reject_bps
        self.submission_count = 0
        self.accepted_count = 0
        self.disputed_count = 0
        self.latest_submission_id = 0
        self.latest_status = "not_submitted"
        self.latest_score = 0
        self.latest_release_bps = 0
        self.latest_evidence_hash = ""
        self.latest_reason = "No milestone evidence submitted"

    @gl.public.view
    def latest_verdict(self) -> str:
        return (
            f"id={self.latest_submission_id};"
            f"status={self.latest_status};"
            f"score={self.latest_score};"
            f"release_bps={self.latest_release_bps};"
            f"evidence_hash={self.latest_evidence_hash};"
            f"reason={self.latest_reason}"
        )

    @gl.public.view
    def progress(self) -> str:
        return (
            f"submissions={self.submission_count};"
            f"accepted={self.accepted_count};"
            f"disputed={self.disputed_count}"
        )

    @gl.public.write
    def submit_milestone(
        self,
        milestone_name: str,
        evidence_json: str,
        evidence_hash: str,
        deterministic_score: int,
    ) -> str:
        if deterministic_score < 0 or deterministic_score > 100:
            raise gl.vm.UserError("deterministic_score must be 0..100")
        if len(evidence_hash) < 16:
            raise gl.vm.UserError("evidence_hash is too short")

        prompt = f"""
        You are a GenLayer validator auditing an AI agent milestone.

        Project:
        {self.project_name}

        Buyer requirements:
        {self.buyer_requirements}

        Milestone:
        {milestone_name}

        Deterministic pre-score:
        {deterministic_score}/100

        Evidence hash:
        {evidence_hash}

        Evidence JSON:
        {evidence_json}

        Decide whether the submitted evidence proves the milestone is complete.
        Evaluate completeness, test evidence, user-facing integration, reproducibility,
        and whether the evidence directly satisfies the buyer requirements.

        Return strict JSON:
        {{
          "status": "accepted" or "revision" or "rejected" or "disputed",
          "score": integer from 0 to 100,
          "release_bps": integer from 0 to 10000,
          "reason": "one concrete technical sentence"
        }}

        Use accepted only for complete work with runnable evidence.
        Use disputed when evidence conflicts or needs human review.
        """

        def leader_fn():
            return gl.nondet.exec_prompt(prompt, response_format="json")

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            mine = leader_fn()
            score_delta = abs(int(mine["score"]) - int(leaders_res.calldata["score"]))
            release_delta = abs(int(mine["release_bps"]) - int(leaders_res.calldata["release_bps"]))
            return (
                mine["status"] == leaders_res.calldata["status"]
                and score_delta <= 8
                and release_delta <= 500
            )

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        status = result["status"]
        score = int(result["score"])
        release = int(result["release_bps"])

        if status not in ["accepted", "revision", "rejected", "disputed"]:
            raise gl.vm.UserError("invalid status")
        if score < 0 or score > 100 or release < 0 or release > 10000:
            raise gl.vm.UserError("invalid score or release_bps")
        if status == "accepted" and release < self.release_bps:
            raise gl.vm.UserError("accepted verdict must meet release threshold")
        if status == "rejected" and release > self.revision_bps:
            raise gl.vm.UserError("rejected verdict cannot release revision-level funds")

        self.submission_count += 1
        self.latest_submission_id = self.submission_count
        self.latest_status = status
        self.latest_score = score
        self.latest_release_bps = release
        self.latest_evidence_hash = evidence_hash
        self.latest_reason = result["reason"]

        if status == "accepted":
            self.accepted_count += 1
        if status == "disputed":
            self.disputed_count += 1

        return self.latest_verdict()
