window.addEventListener("DOMContentLoaded", () => {
    usernames = [...document.getElementsByClassName('username')];
    user_post_button = document.getElementById('show_user_posts');
    usernames.forEach(element => {
        element.addEventListener("click", (val)=>{
            val.target.preventdefault;
            GetInfoAboutUser(val.target.innerText)
        });
    });

        user_post_button.addEventListener("click", (val)=>{
            console.log(val.target);
            GetPosts(val.target.value);
        });
    });

function GetInfoAboutUser(user){
    fetch('/find_user',
    {   method: 'POST', 
        headers:  { 'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'text/html'},
        body:  JSON.stringify({"need_user": user})
    })
    .then(res=>res.json())
    .then(res=>{
        let currentUser = res[0];
        document.getElementById("mod_title").innerHTML += currentUser.name;
        body = document.getElementById('mod_body');
        sp1 = document.createElement('span');
        body.appendChild(sp1);
        document.getElementById('tab_name').innerHTML = currentUser.name;
        document.getElementById('tab_username').innerHTML = currentUser.username;
        document.getElementById('tab_email').innerHTML = currentUser.email;
        document.getElementById('addr_street').innerHTML = currentUser.address.street;
        document.getElementById('addr_suite').innerHTML = currentUser.address.suite;
        document.getElementById('addr_city').innerHTML = currentUser.address.city
        document.getElementById('addr_zipcode').innerHTML = currentUser.address.zipcode;
        document.getElementById('geo_lat').innerHTML = currentUser.address.geo.lat;
        document.getElementById('geo_lng').innerHTML = currentUser.address.geo.lng;
        document.getElementById('com_name').innerHTML = currentUser.company.name;
        document.getElementById('com_phrase').innerHTML = currentUser.company.catchPhrase;
        document.getElementById('com_bs').innerHTML = currentUser.company.bs;
        document.getElementById('com_bs').innerHTML = currentUser.company.bs;
        document.getElementById('show_user_posts').value = currentUser.username;
    })
};

function GetPosts(username){
    window.location.href = `/${username}`;
};

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null
};

