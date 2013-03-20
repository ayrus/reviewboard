// Listener for details link over each extension.
$('.item_actions > a.details').click(function() {
    show_details(this.title, false);
});

// Listener for install link over each extension.
$('.item_actions > a.install').click(function() {
    show_details(this.title, true);
});

function show_details(package_name, open_install_tab){

    var extension_info = new ExtensionInfo({id : package_name});
    extension_info.ready({
        ready: function(){
            console.log(extension_info);
            var modalBoxView = new TabbedModalBoxView({model: extension_info});
            modalBoxView.render(open_install_tab);
        },
        error: function(model, text, statusText){
            // XXX: How to handle this?
            alert(text);
        }
    });
}