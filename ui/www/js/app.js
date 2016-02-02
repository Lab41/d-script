var app = angular.module("app", [
    "ui.router",
    "app.controllers",
    "app.directives",
    "app.services",
    "app.filters"
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
        templateUrl: "templates/main.html",
        controller: "mainCtrl"
    })
    
    // process step
    .state("app.process", {
        url: "{step}",
        templateProvider: function($http, $stateParams) {
            return $http.get("templates/steps/" + $stateParams.step + ".html").then(function(template) {
                return template.data;
            });
        }/*,
        controller: "stepCtrl"*/
    })

    $urlRouterProvider.otherwise("/step-1");

});