const apiUrlInput = document.getElementById("apiUrl");
const saveApiUrlBtn = document.getElementById("saveApiUrl");
const postForm = document.getElementById("postForm");
const postText = document.getElementById("postText");
const postsList = document.getElementById("posts");
const refreshBtn = document.getElementById("refreshBtn");

const DEFAULT_API_URL = "http://localhost:8000";

function getApiUrl() {
  return localStorage.getItem("apiUrl") || DEFAULT_API_URL;
}

function setApiUrl(url) {
  localStorage.setItem("apiUrl", url);
}

async function request(path, options = {}) {
  const response = await fetch(`${getApiUrl()}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Request failed");
  }

  return response.json();
}

async function loadPosts() {
  postsList.innerHTML = "<li>Loading...</li>";
  try {
    const posts = await request("/api/posts");
    postsList.innerHTML = "";

    if (posts.length === 0) {
      postsList.innerHTML = "<li>No posts yet.</li>";
      return;
    }

    for (const post of posts) {
      const item = document.createElement("li");
      item.className = "post";
      item.innerHTML = `
        <div>${post.text}</div>
        <div class="meta">Score: <strong>${post.score}</strong> • Created: ${post.created_at}</div>
      `;

      const upvoteBtn = document.createElement("button");
      upvoteBtn.textContent = "⬆️ Upvote";
      upvoteBtn.onclick = async () => {
        await vote(post.id, 1);
      };

      const downvoteBtn = document.createElement("button");
      downvoteBtn.textContent = "⬇️ Downvote";
      downvoteBtn.onclick = async () => {
        await vote(post.id, -1);
      };

      item.appendChild(upvoteBtn);
      item.appendChild(downvoteBtn);
      postsList.appendChild(item);
    }
  } catch (error) {
    postsList.innerHTML = `<li>Error: ${error.message}</li>`;
  }
}

async function vote(postId, delta) {
  try {
    await request(`/api/posts/${postId}/vote`, {
      method: "POST",
      body: JSON.stringify({ delta }),
    });
    await loadPosts();
  } catch (error) {
    alert(`Vote failed: ${error.message}`);
  }
}

postForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = postText.value.trim();
  if (!text) return;

  try {
    await request("/api/posts", {
      method: "POST",
      body: JSON.stringify({ text }),
    });
    postText.value = "";
    await loadPosts();
  } catch (error) {
    alert(`Create post failed: ${error.message}`);
  }
});

saveApiUrlBtn.addEventListener("click", async () => {
  const url = apiUrlInput.value.trim();
  if (!url) return;
  setApiUrl(url);
  await loadPosts();
});

refreshBtn.addEventListener("click", loadPosts);

apiUrlInput.value = getApiUrl();
loadPosts();
