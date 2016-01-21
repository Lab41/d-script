var app = angular.module("app", [
    "ui.router",
    "app.controllers",
    "app.directives",
    "app.services"
]);

/***********************/
/********* RUN *********/
/***********************/

app.run(function() {
    
    // run methods here
    
});

/**************************/
/********* CONFIG *********/
/**************************/

app.config(function($stateProvider, $urlRouterProvider) {

	/****************/
	/**** ROUTES ****/
	/****************/

	$stateProvider
    
    // main app (shared structure)
    .state("app", {
        url: "/",
        abstract: true,
        templateUrl: "templates/main.html",
        controller: "mainCtrl"
    })
    
    // explore vs explain
    .state("app.viz", {
        url: "{type}",
        templateProvider: function($http, $stateParams) {
            return $http.get("templates/" + $stateParams.type + ".html").then(function(template) {
                return template.data;
            });
        },
        controllerProvider: function($stateParams) {
            return $stateParams.type + "Ctrl"
        }
    })

    $urlRouterProvider.otherwise("/explain");

});