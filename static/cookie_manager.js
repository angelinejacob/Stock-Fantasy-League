function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var scope = angular.element($("#mainNavbar")).scope();
    scope.$apply(function () {
        scope.signedIn = true;
        scope.username = profile.getName();
        scope.imageurl = profile.getImageUrl();
    });
    var scope2 = angular.element($("#loginView")).scope();
    scope2.$apply(function () {
        scope2.showLoginIn = false;
    });
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    var scope = angular.element($("#mainNavbar")).scope();
    auth2.signOut().then(function () {
        scope.$apply(function () {
            scope.username = '';
            scope.imageurl = '';
            scope.signedIn = false;
        });
        console.log('User signed out.');
    });
}

function wantSignIn() {
    var scope = angular.element($("#logInView")).scope();
    scope.$apply(function () {
        scope.showLoginIn = true;
    });
}
