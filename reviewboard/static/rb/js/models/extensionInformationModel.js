ExtensionInfo = RB.BaseResource.extend({
    rspNamespace: 'extension',
    id: null,

    defaults: _.defaults({
        name: null,
        description: null,
        version: null,
        author: null,
        rating: null,
        compatibility: null,
        dependencies: null,
        screenshots: null,
        preinstall: null,
        installed: null
    }, RB.BaseResource.prototype.defaults),

    url: function() {
        return '../../api/extensionbrowser/extensions/' + this.id + '/';
    },

    parse: function(rsp) {

        var result = RB.BaseResource.prototype.parse.call(this, rsp),
            rspData = rsp[this.rspNamespace];

        result.name = rspData.name;
        result.description = rspData.description;
        result.version = rspData.version;
        result.author = rspData.author;
        result.rating = rspData.rating;
        result.compatibility  = rspData.compatibility;
        result.dependencies = rspData.dependencies;
        result.screenshots = rspData.screenshots;
        result.preinstall = rspData.preinstall;
        result.installed = rspData.installed;
        result.install_url = rspData.install_url;

        return result;
    }
});

ExtensionInstallInfo = RB.BaseResource.extend({
    rspNamespace: "install",

    defaults: _.defaults({
        package_name: null,
        install_url: null
    }, RB.BaseResource.prototype.defaults),

    url: function(){
        return '../../api/extensionbrowser/install/';
    },

    toJSON: function(){
        return {
            package_name: this.get('package_name'),
            install_url: this.get('install_url')
        };
    },

    parse: function(rsp) {
    }
});