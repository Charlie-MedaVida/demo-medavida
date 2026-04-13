from guardian.shortcuts import assign_perm
from .models import TokenEventLog, Profile



def subtract_token(user, summary, description):
    event = TokenEventLog.objects.create(
        user=user,
        summary=summary,
        details=description,
        event_type=TokenEventLog.TypeChoices.SUBTRACT
    )
    assign_perm('twitter_pictures.view_spendingevents', user, event)
    assign_perm('twitter_pictures.change_spendingevents', user, event)
    assign_perm('twitter_pictures.delete_spendingevents', user, event)

    # NOTE This can be optimized into a single DB query
    profile = Profile.objects.get(user=user)
    profile.credit_count = profile.credit_count - 1
    profile.save()
