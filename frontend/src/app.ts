const btn = document.getElementById("btn");

btn?.addEventListener("click", async () => {
  const res = await fetch("/api/test");
  const data = await res.json();
  alert(data.message);
});