async function getToken() {
  const r = await fetch("/api/user/Token/", {
    method: "GET",
    headers: {
      "Content-type": "application/json",
    },
  });
  return r.text().then(function (text) {
    return text.toString();
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default { getToken, getCookie };
