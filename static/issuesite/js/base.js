
var appUser;

$(function(){
  // This is the host for the backend.
  // TODO: When running Firenotes locally, set to http://localhost:8081. Before
  // deploying the application to a live production environment, change to
  // https://backend-dot-<PROJECT_ID>.appspot.com as specified in the
  // backend's app.yaml file.
  var backendHostUrl = 'http://localhost:8080';

  // Initialize Firebase
  // TODO: Replace with your project's customized code snippet
  var config = {
    apiKey: "AIzaSyCXLkQ2natcA5XKjOwEt2htv5xgw7uz5KM",
    authDomain: "sourcebase-a547d.firebaseapp.com",
    databaseURL: "https://sourcebase-a547d.firebaseio.com",
    projectId: "sourcebase-a547d",
    storageBucket: "sourcebase-a547d.appspot.com",
    messagingSenderId: "1018666741394"
  };

  // This is passed into the backend to authenticate the user.
  var userIdToken = null;

  // Firebase log-in
  function configureFirebaseLogin() {

    firebase.initializeApp(config);
    //console.log("configurefirebaselogin");
    // console.log(firebase);

    // [START onAuthStateChanged]
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        $('#navbar-signIn').hide();
        $('#signed-in-dropdown').show();
        var profileLink = "/users/" + user.uid + "/";
        $("#my-profile").attr("href", profileLink );
        
        var name = user.displayName;
        currentUser = user;
        //console.log("User:");
        //console.log(currentUser);
        currentUser.getIdToken().then(function(idToken) {
          //console.log(userIdToken);

          //console.log("Token:");
          //console.log(idToken);
          //$('#user').text(welcomeName);
          //$('#logged-in').show();

        });
        /* If the provider gives a display name, use the name for the
        personal welcome message. Otherwise, use the user's email. */
        var welcomeName = name ? name : user.email;



      } else {
        currentUser = null;
        $('#navbar-signIn').show();
        $('#signed-in-dropdown').hide();
        $("#my-profile").attr("href", "/" );


        //$('#logged-in').hide();
        //$('#logged-out').show();

      }
    // [END onAuthStateChanged]

    });

  }

  // [START configureFirebaseLoginWidget]
  // Firebase log-in widget
  function configureFirebaseLoginWidget() {
    // console.log("widgeeeet");
    var uiConfig = {
      callbacks: {
        signInSuccess: function(currentUser, credential, redirectUrl) {
          // console.log("signed in...");
          // console.log(redirectUrl);
          // User successfully signed in.
          // Return type determines whether we continue the redirect automatically
          // or whether we leave that to developer to handle.
          currentUser.getIdToken().then(function(idToken) {
                    //console.log(userIdToken);
                    //console.log("Token:");
                    //console.log(idToken);
                    //$('#user').text(welcomeName);
                    //$('#logged-in').show();
                    verifyOrCreateUser(idToken, currentUser.uid);


                  });


          function verifyOrCreateUser(userIdToken, userID) {
            //console.log(userIdToken);
            $.ajax('/verifyOrCreateUser/', {
              /* Set header for the XMLHttpRequest to get data from the web server
              associated with userIdToken */
              headers: {
                'Authorization': 'Bearer ' + userIdToken
              }
            }).then(function(data){
              $('#name').empty();
              // console.log(data);
              // Iterate over user data to display user's notes from database.
              console.log(JSON.parse(data))
            });
          }
          return false;
        },
        uiShown: function() {
          // The widget is rendered.
          // Hide the loader.
        }
      },
      // Will use popup for IDP Providers sign-in flow instead of the default, redirect.
      //signInFlow: 'popup',
      //signInSuccessUrl: '/',
      signInOptions: [
        // Leave the lines as is for the providers you want to offer your users.
        {
          provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
          scopes: [
            'https://www.googleapis.com/auth/plus.login'
          ],
          customParameters: {
            // Forces account selection even when one account
            // is available.
            prompt: 'select_account'
          }
        },
        {
          provider: firebase.auth.FacebookAuthProvider.PROVIDER_ID,
          scopes: [
            'public_profile',
            'email',
            'user_likes',
            'user_friends'
          ],
          customParameters: {
            // Forces password re-entry.
            auth_type: 'reauthenticate'
          }
        },
        firebase.auth.TwitterAuthProvider.PROVIDER_ID,
        firebase.auth.GithubAuthProvider.PROVIDER_ID,
        // firebase.auth.EmailAuthProvider.PROVIDER_ID,
        // firebase.auth.PhoneAuthProvider.PROVIDER_ID
      ],
      // Terms of service url.
      tosUrl: '<your-tos-url>'
    };
    try {
        ui = new firebaseui.auth.AuthUI(firebase.auth());
    }
    catch(err) {
        console.log("App already exists, but it's ok!")
    }
    
    ui.start('#firebaseui-auth-container', uiConfig);
  }
  // [END configureFirebaseLoginWidget]

  // [START signOutBtn]
  // Sign out a user
  var signOutBtn =$('#sign-out');
  signOutBtn.click(function(event) {
    event.preventDefault();

    firebase.auth().signOut().then(function() {
      // console.log("Sign out successful");
    }, function(error) {
      // console.log(error);
    });
  });
  // [END signOutBtn]
  //console.log(userIdToken);

  configureFirebaseLogin();
  configureFirebaseLoginWidget();


    firebase.auth().onAuthStateChanged(function(user) {
      appUser = user;
    });

  var signOutBtn2 = $('#sign-out-2');
  signOutBtn2.click(function(event) {
    event.preventDefault();

    firebase.auth().signOut().then(function() {
      console.log("Sign out successful");
      configureFirebaseLoginWidget();
    }, function(error) {
      console.log(error);
    });
  });
});


// TODO: afer login, the login modal does not reinitialize with its content, and stays empty. 
// If signed in, and sign out is clicked, sign out is sucessful, but modal still isnt initialized, 
// and page must be refreshed before new sign in. Page neeeding to be refreshed suggests that 
// base.js needs to run again. does it not run after sign in? seems not. think about and fix.