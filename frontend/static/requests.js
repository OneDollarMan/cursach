async function loginUser() {
    var params = new URLSearchParams();
    params.set('username', document.getElementById('loginEmail').value);
    params.set('password', document.getElementById('loginPassword').value);

    const res = await fetch('/api/auth/jwt/login', {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: params
    })
    if(res.ok) {
        window.location.replace("/explore");
    }
}

async function registerUser() {
    data = {
        email: document.getElementById('email').value,
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        password: document.getElementById('password').value,
    }

    const res = await fetch('/api/auth/register', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })

    if(res.ok) {

    }
}

async function logoutUser() {
    const res = await fetch('/api/auth/jwt/logout', {
        method: "POST",
    })
    if(res.ok) {
        window.location.replace("/");
    }
}

async function subscribeUser(event) {
    event.preventDefault()
    const formData = new FormData(event.target);
    data = {
        author_id: formData.get('author_id'),
        subscription_level_id: formData.get('subscription_level_id')
    }

    const res = await fetch('/api/subscribe', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    if(res.ok) {

    }
}

async function unsubscribeUser(event) {
    event.preventDefault()
    const formData = new FormData(event.target);
    data = {
        author_id: formData.get('author_id'),
        subscription_level_id: formData.get('subscription_level_id')
    }

    const res = await fetch('/api/unsubscribe', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    if(res.ok) {

    }
}

async function addSubscriptionLevel(event) {
    event.preventDefault()
    const formData = new FormData(event.target);
    data = {
        title: formData.get('title'),
        is_chat_available: formData.get('is_chat_available')
    }
    if(data.is_chat_available == null) {
        data.is_chat_available = false
    }

    const res = await fetch('/api/subscription_levels', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    if(res.ok) {
        window.location.replace("/profile");
    }
}

async function addArticle(event) {
    event.preventDefault()
    const formData = new FormData(event.target);
    data = {
        title: formData.get('title'),
        content: formData.get('content'),
        subscription_level_id: formData.get('subscription_level_id')
    }

    const res = await fetch('/api/articles', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    if(res.ok) {
        window.location.replace("/articles");
    }
}