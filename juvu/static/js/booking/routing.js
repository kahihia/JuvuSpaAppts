//-------------------------------------------------------
// Route URLs.
//

var routey = Backbone.Router.extend({

    routes: {
        "toc": "toc",
        "treething": "treething",
        "calendar": "calendar",
        "step/:num": "step",
    },

    toc: function() {
        viewModel.viewing("toc");
    },

    treething: function() {
        viewModel.viewing("treething");
    },

    calendar: function() {
        viewModel.viewing("calendar");
    },

    step: function(num) {
        num = +num;
        if (num >= 0 && num <= 4) {
            viewModel.viewing(num);
        } else {
            routes.navigate("toc", true);
        }
    },

});

