var ArticleList = [];

var Users = [];

var articleList = document.querySelector("#article-list");

var histButton = document.querySelector("#historybutton");

var homeButton = document.querySelector("#homebutton");

var settButton = document.querySelector("#settingsbutton");

var libButton = document.querySelector("#liberalbutton");

var indButton = document.querySelector("#independentbutton");

var consButton = document.querySelector("#conservativebutton");

var signupButton = document.querySelector("#signupbutton");

var loginButton = document.querySelector("#loginbutton");

var createsigninButton = document.querySelector("#createsigninbutton");

var signinButton = document.querySelector("#signinbutton");

var readingArticle = document.querySelector("#articles");

var titleArticle = document.querySelector("#articlesTitle");

var sourceArticle = document.querySelector("#articlesSource");

var linkButton = document.querySelector("#articlelink")

var mainPage = document.querySelector(".mains");

var readingPage = document.querySelector(".readings");

var signupPage = document.querySelector("#signup");

var loginPage = document.querySelector("#login");

histButton.onclick = function () {
    window.alert("History functionality not yet implemented.");
};

settButton.onclick = function () {
    window.alert("Settings functionality not yet implemented.");
};

homeButton.onclick = function () {
    location.href = "home.html"
};

signupButton.onclick = function() {
    location.href = "signup.html"
};

loginButton.onclick = function() {
    readingPage.style.display = "none";
    articleList.style.display = "none";
    loginPage.style.display = "block";
    signupPage.style.display = "none";
};

signinButton.onclick = function() {
    var lemailTextField = document.querySelector("#lemail");
    var lemail = lemailTextField.value; 

    var lpasswordTextField = document.querySelector("#lpassword");
    var lpassword = lpasswordTextField.value; 

    lemailTextField.value = "";
    lpasswordTextField.value = "";
    var data = "lemail=" + encodeURIComponent(lemail);
    data += "&lpassword=" + encodeURIComponent(lpassword);
    fetch("http://0.0.0.0:5000/sessions", {
        method: 'POST',
        credentials: 'include',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        if (response.status == 401) {
            window.alert("Email or Password incorrect");}
        else if (response.status == 201) {
            window.alert("You have successfully logged in!");
        } else {
            window.alert("Unexpected error logging in.");
        }
    });
};

createsigninButton.onclick = function () {
    var snameTextField = document.querySelector("#sfname");
    var sname = snameTextField.value; 

    var slnameTextField = document.querySelector("#slname");
    var slname = slnameTextField.value; 

    var sageTextField = document.querySelector("#sage");
    var sage = sageTextField.value;

    var semailTextField = document.querySelector("#semail");
    var semail = semailTextField.value;

    var spasswordTextField = document.querySelector("#spassword");
    var spassword = spasswordTextField.value;

    var cspasswordTextField = document.querySelector("#cspassword");
    var cspassword = cspasswordTextField.value;
    if (spassword == cspassword) {
        snameTextField.value = "";
        slnameTextField.value = "";
        sageTextField.value = "";
        semailTextField.value = "";
        spasswordTextField.value = "";
        cspasswordTextField.value = "";
        var data = "sfname=" + encodeURIComponent(sname);
        data += "&slname=" + encodeURIComponent(slname);
        data += "&sage=" + encodeURIComponent(sage);
        data += "&semail=" + encodeURIComponent(semail);
        data += "&cspassword=" + encodeURIComponent(spassword);
        fetch("http://localhost:5000/users", {
            method: 'POST',
            credentials: 'include',
            body: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function (response) {
            if (response.status == 422){
                window.alert("User already exists.");}
            else if (response.status == 201) {
                window.alert("You have successfully registered! Please login.");
                readingPage.style.display = "none";
                articleList.style.display = "block";
                loginPage.style.display = "none";
                signupPage.style.display = "none";}
            else{
                window.alert("Unexpected error registering.");
            }
        });
    } else {
        window.alert("Passwords didn't match.")
        spasswordTextField.value = "";
        cspasswordTextField.value = "";
    }
};

function loadArticlesFromServer() {
    fetch("/articles").then(function (response) {
        response.json().then(function (data) {
            ArticleList = data;
            articleList.innerHTML = "";
            ArticleList.forEach(function (article){
                var newListItem = document.createElement("li");
                var articleTitleButton = document.createElement("button");
                articleTitleButton.innerHTML = article.source1 + ": " + " " + " " + " " + article.title1;
                console.log(article.title);
                articleTitleButton.classList.add("article-title");
                articleTitleButton.onclick = function () {
                    mainPage.style.display = "none";
                    readingPage.style.display = "block";
                    readingArticle.innerHTML = article.story1;
                    titleArticle.innerHTML = article.title1;
                    linkButton.href = article.url1;
                    sourceArticle.innerHTML = "Source: " +article.source1;
                    libButton.onclick = function(){
                        if (article.source1 == "NBC") {
                            readingArticle.innerHTML = article.story1;
                            titleArticle.innerHTML = article.title1;
                            linkButton.href = article.url1;
                            sourceArticle.innerHTML = "Source: " + article.source1;
                        } else if (article.source2 == "NBC") {
                            readingArticle.innerHTML = article.story2;
                            titleArticle.innerHTML = article.title2;
                            sourceArticle.innerHTML = "Source: " +article.source2;
                            linkButton.href = article.url2;
                         } else if (article.source3 == "NBC") {
                             readingArticle.innerHTML = article.story3;
                             titleArticle.innerHTML = article.title3;
                             linkButton.href = article.url3;
                             sourceArticle.innerHTML = "Source: " +article.source3;
                         } 
                    };
                    indButton.onclick = function(){
                        if (article.source1 == "AP") {
                            readingArticle.innerHTML = article.story1;
                            titleArticle.innerHTML = article.title1;
                            linkButton.href = article.url1;
                            sourceArticle.innerHTML = "Source: " + article.source1;
                        } else if (article.source2 == "AP") {
                            readingArticle.innerHTML = article.story2;
                            titleArticle.innerHTML = article.title2;
                            linkButton.href = article.url2;
                            sourceArticle.innerHTML = "Source: " + article.source2;
                        } else if (article.source3 == "AP") {
                            readingArticle.innerHTML = article.story3;
                            titleArticle.innerHTML = article.title3;
                            linkButton.href = article.url3;
                            sourceArticle.innerHTML = "Source: " + article.source3;
                        } 
                    };
                    consButton.onclick = function(){
                        if (article.source1 == "Fox") {
                            readingArticle.innerHTML = article.story1;
                            titleArticle.innerHTML = article.title1;
                            linkButton.href = article.url1;
                            sourceArticle.innerHTML = "Source: " + article.source1;
                        } else if (article.source2 == "Fox") {
                            readingArticle.innerHTML = article.story2;
                            titleArticle.innerHTML = article.title2;
                            linkButton.href = article.url2;
                            sourceArticle.innerHTML = "Source: " + article.source2;
                        } else if (article.source3 == "Fox") {
                            readingArticle.innerHTML = article.story3;
                            titleArticle.innerHTML = article.title3;
                            linkButton.href = article.url3;
                            sourceArticle.innerHTML = "Source: " + article.source3;
                        }
                    };
                };
                newListItem.appendChild(articleTitleButton);
                articleList.appendChild(newListItem);
            });
        });
    });
};

loadArticlesFromServer();