/* This variable is controlled by gulp. You can run gulp with flag -e to set this variable.
Example: gulp dev-cis -e qa
Possible values for flag -e are: 'docker', 'local', 'prod', 'qa', 'dev' (default). */
var env = 'docker';

/************************************
 * ENV URLS
 ************************************/
let ENV_URLS = {}

if (env == "local") {
    ENV_URLS = {
        "api": "http://localhost:8000/api/v1.0/",
        // "apiv2": "http://localhost:8000/api/v2.0/"
    }
} else if (env == "docker") {
    ENV_URLS = {
        "api": "http://localhost:8002/api/v1.0/",
    }
}
else if (env == "production" || env == "staging") {
    alert("No URLs set for for production or staging")
}
else {
    alert("NO ENV SET!")
    console.error("No env set! Using localhost for dev server.");
    ENV_URLS = {
        "api": "https://localhost:8000/api/v1.0/",
    }
}

export const URLS = ENV_URLS

/************************************
 * TODO: UPDATE ALL LOCAL DATA STRINGS
 ************************************/
export const LOCAL = {
    userAuthData: "userAuthData"
};



