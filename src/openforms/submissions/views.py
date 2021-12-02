import logging
import uuid

from django.core.exceptions import PermissionDenied
from django.views.generic import RedirectView

from furl import furl
from rest_framework.reverse import reverse

from .models import Submission
from .tokens import submission_resume_token_generator
from .utils import add_submmission_to_session

logger = logging.getLogger(__name__)


class ResumeSubmissionView(RedirectView):
    def get_redirect_url(self, submission_uuid: uuid, token: str, *args, **kwargs):
        try:
            submission = Submission.objects.get(uuid=submission_uuid)
        except Submission.DoesNotExist:
            logger.debug(
                "Called endpoint with an invalid submission uuid: %s", submission_uuid
            )
            raise PermissionDenied("Resume url is not valid")

        # Check that the token is valid
        valid = submission_resume_token_generator.check_token(submission, token)
        if not valid:
            logger.debug("Called endpoint with an invalid token: %s", token)
            raise PermissionDenied("Resume submission url is not valid")

        form_resume_url = furl(submission.form_url)
        # furl adds paths with the /= operator
        form_resume_url /= "stap"
        form_resume_url /= (
            submission.get_last_completed_step().form_step.form_definition.slug
        )
        # Add the submission uuid to the query param
        form_resume_url.add({"submission_uuid": submission.uuid})

        # No login required, skip authentication
        if not submission.form.login_required:
            add_submmission_to_session(submission, self.request.session)
            return form_resume_url.url

        # Login IS required. Check if the user has already logged in.
        # This is done by checking if the authentication details are in the session and
        # if they match those in the saved submission.
        if "form_auth" in self.request.session:
            if not self._is_auth_data_correct(submission):
                raise PermissionDenied("Authentication data is not valid")

            add_submmission_to_session(submission, self.request.session)
            return form_resume_url.url

        # The user has not logged in. Redirect them to the start of the authentication process
        auth_start_url = reverse(
            "authentication:start",
            request=self.request,
            kwargs={"slug": submission.form.slug, "plugin_id": submission.auth_plugin},
        )

        redirect_url = furl(auth_start_url)
        redirect_url.args["next"] = reverse(
            "submissions:resume",
            request=self.request,
            kwargs={"submission_uuid": submission.uuid, "token": token},
        )

        return redirect_url.url

    def _is_auth_data_correct(self, submission: Submission) -> bool:
        is_auth_plugin_correct = (
            submission.auth_plugin == self.request.session["form_auth"]["plugin"]
        )
        submission_auth_value = getattr(
            submission, self.request.session["form_auth"]["attribute"]
        )
        is_auth_data_correct = (
            submission_auth_value == self.request.session["form_auth"]["value"]
        )

        return is_auth_plugin_correct and is_auth_data_correct
