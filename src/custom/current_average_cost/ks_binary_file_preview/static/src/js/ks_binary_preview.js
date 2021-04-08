odoo.define('ks_binary_file_preview.ks_binary_preview', function(require){

    var BasicFields = require('web.basic_fields');
    var DocumentViewer = require('mail.DocumentViewer');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var ks_file_data = undefined;

    BasicFields.FieldBinaryFile.include({

        events: _.extend({}, BasicFields.FieldBinaryFile.prototype.events, {
            'click .ks_binary_file_preview': "ks_onAttachmentView",
        }),

        _renderReadonly: function(){
            var self = this;
            self._super.apply(this,arguments);
            if (!self.res_id) {
                self.$el.css('cursor', 'not-allowed');
            } else {
                self.$el.css('cursor', 'pointer');
                self.$el.attr('title', 'Download');
            }
            self.$el.append(core.qweb.render("ks_preview_button"));
        },

        ks_onAttachmentView: function(ev){
            var self = this;
            try {
                ev.preventDefault();
                ev.stopPropagation();
                var ks_mimetype = this.recordData.mimetype;

                function ks_docView(ks_file_data){
                    if(ks_file_data){
                        var ks_attachment = [{
                            filename: ks_file_data.name,
                            id: ks_file_data.id,
                            is_main: false,
                            mimetype: ks_file_data.type,
                            name: ks_file_data.name,
                            type: ks_file_data.type,
                            url: "/web/content/" + ks_file_data.id + "?download=true",
                        }]
                        var ks_activeAttachmentID = ks_file_data.id;
                        var ks_attachmentViewer = new DocumentViewer(self, ks_attachment, ks_activeAttachmentID);
                        ks_attachmentViewer.appendTo($('body'));
                    }
                }
                if(ks_mimetype){
                    ks_file_data = {
                        'id' : this.recordData.id,
                        'type' : this.recordData.mimetype || 'application/octet-stream',
                        'name' :  this.recordData.name || this.recordData.display_name || "",
                    }
                    ks_docView(ks_file_data);
                }
                else{
                    var def = ajax.jsonRpc("/get/record/details", 'call',{
                        'res_id': this.res_id,
                        'model': this.model,
                        'size': this.value,
                        'res_field': this.field.string || this.name,
                    });
                }

                return $.when(def).then(function(vals){
                    if (vals){
                        ks_docView(vals);
                    }
                });
            }
            catch(err) {
                alert(err);
            }
        },
    });
});
