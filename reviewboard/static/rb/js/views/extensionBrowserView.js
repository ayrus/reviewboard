TabbedModalBoxView = Backbone.View.extend({

    el: $("<div/>"),

    initialize: function(){
        _.bindAll(this, 'render');
    },

    render: function(show_install_tab){

        var template_html = '\
         <div id="extension_info_tabs" class="extensionbrowser">\
          <ul>\
           <li><a href="#ext-information">Information</a></li>\
           <li><a href="#ext-screenshots">Screenshots</a></li>\
           <li><a href="#ext-dependencies">Dependencies</a></li>\
           <li><a href="#ext-preinstall">Install</a></li>\
          </ul>\
          <div id="ext-information">\
          </div>\
          <div id="ext-screenshots">\
          </div>\
          <div id="ext-dependencies">\
          </div>\
          <div id="ext-preinstall">\
          </div>\
         </div>';

        var template = _.template(template_html, {name: this.model.get('name')});
        $(this.el).html(template);
        $(this.el).addClass("extensions_modalbox");
        $(this.el).modalBox();

        var info_view = new InfoView({ model: this.model });
        var current_tab = show_install_tab ? 3 : 0;
        // Populate the first or install tab.
        info_view.render(current_tab);

        $("#extension_info_tabs").tabs({

            selected: current_tab,

            select: function(e, ui){
                info_view.render(ui.index);
            }
        });

        return this;
    }
});

InfoView = Backbone.View.extend({

    el: $("<div/>"),

    initialize: function(){
        _.bindAll(this, 'render');
    },

    events: {
        "click .extension_info_wrapper > button": "install"
    },

    render: function(tab_index){

        var template_html = this.get_template(tab_index);
        var template = _.template(template_html, this.model.attributes)
        $(this.el).html(template);
        $("#" + this.get_target(tab_index)).html(this.el);
    },

    install: function(){
        var extension_install = new ExtensionInstallInfo({
                                    package_name: this.model.get('id'),
                                    install_url: this.model.get('install_url')
                                });

        extension_install.save({
            success: function(){
                // TODO: Change UI to reflect installation.
                alert('done');
            },
            error: function(model, text, statusText){
                // QUESTION: How to handle this?
            }
        });
    },

    get_target: function(tab_index){

        var targets = new Array("ext-information", "ext-screenshots", "ext-dependencies", "ext-preinstall");
        return targets[tab_index];
    },

    get_template: function(tab_index){

        var info_template = '\
        <div class="extension_info_wrapper">\
         <div class="extension_info_main">\
          <span class="extension_title"><%= name %></span>\
          <label>Description</label>:\
          <div class="extension_text">\
           <%= description %>\
          </div>\
         </div>\
         <div class="extension_info_sidebar">\
          <div><label>Author</label>: <%= author %></div>\
          <div><label>Version</label>: <%= version %></div>\
          <div><label>Rating</label>: <%= rating %></div>\
          <div><label>Compatibility</label>: <%= compatibility.start %> - <%= compatibility.end %></div>\
         </div>\
         <div class="clear"></div>\
        </div>';

        var screenshots = '\
        <div class="extension_info_wrapper">\
         <div class="extension_screenshots">\
         <span class="extension_title"><%= name %></span>\
         <% _.each(screenshots, function(screenshot){ %>\
          <a href="<%= screenshot.image %>" target="_blank">\
           <img src="<%= screenshot.thumbnail %>" class="extension_screenshot_img" />\
          </a>\
         <% }); %>\
         </div>\
        </div>';

        var dependencies = '\
        <div class="extension_info_wrapper">\
         <span class="extension_title"><%= name %></span>\
         <ul>\
          <% _.each(dependencies, function(dependency){ %>\
            <li>\
             <%= dependency.name %> (<a href="<%= dependency.url %>"><%= dependency.package %></a>)\
            </li>\
          <% }); %>\
         </ul>\
        </div>';

        var pre_install = '\
        <div class="extension_info_wrapper">\
         <span class="extension_title"><%= name %></span>\
          <label>Pre-Install Information</label>:\
          <div class="extension_text">\
           <%= preinstall %>\
          </div>\
          <% if(installed){ %>\
            <button disabled="disabled">Installed</b>\
          <% }else{ %>\
            <button>Install</button>\
          <% } %>\
        </div>';

        var templates = new Array(info_template, screenshots, dependencies, pre_install);
        return templates[tab_index];
    }
});