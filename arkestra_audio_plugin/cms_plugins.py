from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.contrib import admin, messages
from models import AudioPlayerItem, AudioPlayerPlugin



class AudioPlayerItemInline(admin.TabularInline):
    model = AudioPlayerItem
    extra = 1
	#    fieldset_basic = ('', {'fields': (('image',),)})
	#    fieldset_advanced = ('Caption', {'fields': (( 'use_description_as_caption', 'caption'),), 'classes': ('collapse',)})
	#    fieldsets = (fieldset_basic, fieldset_advanced,         
	#                ("Link", {
	#                    'fields': (('destination_content_type', 'destination_object_id',), 'alt_text',),
	#                    'classes': ('collapse',),
	#            }),
	# )
    # formfield_overrides = {
    #     models.TextField: {'widget': forms.Textarea(attrs={'cols':30, 'rows':3,},),},
    # }


class AudioPlayerPublisher(CMSPluginBase):
    model = AudioPlayerPlugin
    name = _(u"Audio Player")
    text_enabled = True
    raw_id_fields = ('audio',)
    inlines = (AudioPlayerItemInline,)
    admin_preview = False         
    # fieldset_basic = ('Size & proportions', {'fields': (('kind', 'width', 'aspect_ratio',),)})
    # fieldset_advanced = ('Advanced', {'fields': (( 'float', 'height'),), 'classes': ('collapse',)})
    # fieldset_items_per_row = ('For Multiple and Lightbox plugins only', {'fields': ('items_per_row',), 'classes': ('collapse',)})
    # fieldsets = (fieldset_basic, fieldset_items_per_row, fieldset_advanced)
    
    def __init__(self, model = None, admin_site = None):
        self.admin_preview = False
        self.text_enabled = True
        super(AudioPlayerPublisher, self).__init__(model, admin_site)

    def render(self, context, audioplayer, placeholder):

        # don't do anything if there are no files in the audioplayer
        if audioplayer.audioplayer_items.count():
            # calculate the width of the block the templ will be in
            #audioplayer.container_width = width_of_image_container(context, imageset)
            audioplayer.items = audioplayer.audioplayer_items.all()
            audioplayer.number_of_items = audioplayer.audioplayer_items.count()
            
            # at least three items are required for a slider - just two is unaesthetic
            if audioplayer.kind == AudioPlayerPlugin.KIND_PLAYLIST and audioplayer.number_of_items > 1:
                # audioplayer = playlist(audioplayer)
                audioplayer.template = "arkestra_audio_plugin/playlist.html"
            else:
            	audioplayer.template = "arkestra_audio_plugin/single.html"
                audioplayer.item = audioplayer.audioplayer_items.all()[0]

            self.render_template = audioplayer.template
            context.update({
                'audioplayer': audioplayer,
            })
        # no items, use a null template    
        else:
            # print "using a null template" , imageset
            self.render_template = "null.html"  
        return context

            
    def __unicode__(self):
        return self

plugin_pool.register_plugin(AudioPlayerPublisher)
