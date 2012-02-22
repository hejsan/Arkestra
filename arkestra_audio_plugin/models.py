from django.utils.translation import ugettext_lazy as _
from django.db import models
from cms.models import CMSPlugin
from filer.fields.file import FilerFileField

# class AudioFile(CMSPlugin):
#     audio = FilerFileField()
#     def __unicode__(self):
#         if self.audio:
#             return self.audio.label
#         else:
#             return u"Audio Publication %s" % self.caption
#         return ''

class AudioPlayerPlugin(CMSPlugin):
    KIND_PLAYLIST = "playlist"
    KIND_SINGLE = "single"
    PLAYER_KINDS = (
        (KIND_PLAYLIST, _(u"Player with playlist")),
        (KIND_SINGLE,   _(u"Player without playlist")),
        # TODO: link player
    )
    kind = models.CharField(choices = PLAYER_KINDS, max_length = 50, default = PLAYER_KINDS[0][0])
    def __unicode__(self):
        return u"audio-player-%s" % self.kind
    
class AudioPlayerItem(models.Model):
    plugin  = models.ForeignKey(AudioPlayerPlugin, related_name="audioplayer_items")
    audio   = FilerFileField()
    title   = models.CharField(_(u"Title"),  max_length=255, blank=True, null=True)
    artist  = models.CharField(_(u"Artist"), max_length=255, blank=True, null=True)

    def __unicode__(self):
        if self.title and self.artist:
            return u"Audio file: %s - %s" % (self.title, self.artist)
        elif self.title:
            return u"Audio file: %s" % self.title
        elif self.audio:
            return self.audio.label
        return u"Audio file - %i" % self.id
