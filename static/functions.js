function required() {
    var element = document.getElementById("submit").value;
    if (element == "") {
        let warn = "<br><br><h2>Please input a playlist link.</h2>";
        document.getElementById("contentContainer").innerHTML += warn;
        return false;
    }
    return true;
}