const API_URL = "https://1mxd03e34i.execute-api.ap-southeast-2.amazonaws.com/notes";

const userIdInput = document.getElementById("user-id");
const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");
const createStatus = document.getElementById("create-status");

const userIdListInput = document.getElementById("user-id-list");
const listStatus = document.getElementById("list-status");
const notesList = document.getElementById("notes-list");
const notesCount = document.getElementById("notes-count");


async function callApi(payload) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const statusCode = res.status;

  let body;
  try {
    body = await res.json();
  } catch (e) {
    body = { message: "Failed to parse response" };
  }

  return { statusCode, body };
}


document.getElementById("btn-create").addEventListener("click", async () => {
  const userId = userIdInput.value.trim();
  const title = titleInput.value.trim();
  const content = contentInput.value.trim();

  createStatus.textContent = "";
  createStatus.className = "status";

  if (!userId || !title || !content) {
    createStatus.textContent = "userId, title and content are required.";
    createStatus.classList.add("err");
    return;
  }

  try {
    createStatus.textContent = "Creating note...";
    const payload = {
      action: "create",
      body: { userId, title, content }
    };
    const result = await callApi(payload);

    if (result.statusCode === 201) {
      createStatus.textContent = "Note created successfully.";
      createStatus.classList.add("ok");
      titleInput.value = "";
      contentInput.value = "";
    } else {
      createStatus.textContent = result.body?.message || "Failed to create note.";
      createStatus.classList.add("err");
    }
  } catch (err) {
    createStatus.textContent = err.message || "Error calling API.";
    createStatus.classList.add("err");
  }
});


document.getElementById("btn-refresh").addEventListener("click", async () => {
  const userId = userIdListInput.value.trim();

  listStatus.textContent = "";
  listStatus.className = "status";

  if (!userId) {
    listStatus.textContent = "userId is required.";
    listStatus.classList.add("err");
    return;
  }

  try {
    listStatus.textContent = "Loading notes...";
    const payload = {
      action: "list",
      body: { userId }
    };

    const result = await callApi(payload);

    if (result.statusCode === 200) {
      const notes = result.body?.notes || [];
      notesList.innerHTML = "";
      notesCount.textContent = `${notes.length} note${notes.length === 1 ? "" : "s"}`;

      notes.forEach(note => {
        const div = document.createElement("div");
        div.className = "note-item";

        const title = document.createElement("div");
        title.className = "note-title";
        title.textContent = note.title || "(no title)";

        const meta = document.createElement("div");
        meta.className = "note-meta";
        meta.textContent = `${note.userId} · ${note.createdAt}`;

        const content = document.createElement("div");
        content.className = "note-content";
        content.textContent = note.content;

        div.appendChild(title);
        div.appendChild(meta);
        div.appendChild(content);
        notesList.appendChild(div);
      });

      listStatus.textContent = "Notes loaded.";
      listStatus.classList.add("ok");
    } else {
      listStatus.textContent = result.body?.message || "Failed to load notes.";
      listStatus.classList.add("err");
    }
  } catch (err) {
    listStatus.textContent = err.message || "Error calling API.";
    listStatus.classList.add("err");
  }
});
