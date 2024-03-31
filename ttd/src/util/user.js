async function checkLoggedIn() {
  const r = await fetch("/api/account/isLoggedIn/", {
    method: "GET",
    headers: {
      "Content-type": "application/json",
    },
  });
  return r.json().then(function (data) {
    return data;
  });
}

export default { checkLoggedIn };