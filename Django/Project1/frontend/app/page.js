"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

const API_URL = `${
  (process.env.NEXT_PUBLIC_DJANGO_API_URL || "http://localhost:8000").replace(
    /\/+$/,
    "",
  )
}/api/posts/`;

const emptyForm = {
  title: "",
  slug: "",
  body: "",
  status: "DF",
  author: "",
};

async function request(url, options) {
  const response = await fetch(url, options);

  if (!response.ok) {
    const responseBody = await response.text();
    let errorMessage = responseBody;

    try {
      const payload = JSON.parse(responseBody);
      errorMessage = Object.entries(payload)
        .map(([field, messages]) => {
          const description = Array.isArray(messages)
            ? messages.join(" ")
            : messages;
          return `${field}: ${description}`;
        })
        .join(" ");
    } catch {
      if (!errorMessage) {
        errorMessage = `Request failed with status ${response.status}.`;
      }
    }

    throw new Error(errorMessage || `Request failed with status ${response.status}.`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function formatDate(value) {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const loadPosts = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const data = await request(API_URL);
      setPosts(data);
    } catch (loadError) {
      setError(`Could not load posts. ${loadError.message}`);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    request(API_URL)
      .then((data) => setPosts(data))
      .catch((loadError) => {
        setError(`Could not load posts. ${loadError.message}`);
      })
      .finally(() => setLoading(false));
  }, []);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((currentForm) => ({ ...currentForm, [name]: value }));
  }

  function resetForm() {
    setForm(emptyForm);
    setEditingId(null);
  }

  function editPost(post) {
    setForm({
      title: post.title,
      slug: post.slug,
      body: post.body,
      status: post.status,
      author: String(post.author),
    });
    setEditingId(post.id);
    setError("");
    setNotice("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function savePost(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setNotice("");

    const payload = {
      ...form,
      author: Number(form.author),
    };
    const url = editingId === null ? API_URL : `${API_URL}${editingId}/`;

    try {
      await request(url, {
        method: editingId === null ? "POST" : "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setNotice(editingId === null ? "Post created." : "Post updated.");
      resetForm();
      await loadPosts();
    } catch (saveError) {
      setError(`Could not save post. ${saveError.message}`);
    } finally {
      setSaving(false);
    }
  }

  async function deletePost(post) {
    if (!window.confirm(`Delete "${post.title}"? This cannot be undone.`)) {
      return;
    }

    setDeletingId(post.id);
    setError("");
    setNotice("");

    try {
      await request(`${API_URL}${post.id}/`, { method: "DELETE" });
      if (editingId === post.id) {
        resetForm();
      }
      setNotice("Post deleted.");
      await loadPosts();
    } catch (deleteError) {
      setError(`Could not delete post. ${deleteError.message}`);
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <main className="page-shell">
      <header className="topbar">
        <Link className="brand" href="/" aria-label="Inkspot home">
          <span className="brand-mark">i.</span>
          <span>inkspot</span>
        </Link>
        <span className="topbar-note">A little space for your ideas</span>
      </header>

      <section className="intro">
        <p className="eyebrow">YOUR BLOG, YOUR WORDS</p>
        <h1>Make room for a good story.</h1>
        <p className="intro-copy">
          Write something new, or pick up where you left off.
        </p>
      </section>

      <div className="content-grid">
        <section className="editor-panel" aria-labelledby="editor-title">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">{editingId === null ? "THE EDITOR" : "EDITING"}</p>
              <h2 id="editor-title">
                {editingId === null ? "New post" : "Update your post"}
              </h2>
            </div>
            {editingId !== null && (
              <button className="text-button" type="button" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>

          <form className="post-form" onSubmit={savePost}>
            <label>
              Title
              <input
                autoComplete="off"
                maxLength={250}
                name="title"
                onChange={updateField}
                placeholder="Give your post a title"
                required
                value={form.title}
              />
            </label>

            <label>
              Slug
              <input
                autoComplete="off"
                maxLength={250}
                name="slug"
                onChange={updateField}
                placeholder="a-short-url-name"
                required
                value={form.slug}
              />
            </label>

            <label>
              Your post
              <textarea
                name="body"
                onChange={updateField}
                placeholder="Start writing here..."
                required
                rows={9}
                value={form.body}
              />
            </label>

            <div className="form-row">
              <label>
                Status
                <select name="status" onChange={updateField} value={form.status}>
                  <option value="DF">Draft</option>
                  <option value="PB">Published</option>
                </select>
              </label>

              <label>
                Author ID
                <input
                  min="1"
                  name="author"
                  onChange={updateField}
                  placeholder="e.g. 1"
                  required
                  type="number"
                  value={form.author}
                />
              </label>
            </div>
            <p className="field-hint">
              Enter the ID of an existing Django user.
            </p>

            <button className="primary-button" disabled={saving} type="submit">
              {saving
                ? "Saving..."
                : editingId === null
                  ? "Create post"
                  : "Save changes"}
            </button>
          </form>
        </section>

        <section className="posts-panel" aria-labelledby="posts-title">
          <div className="panel-heading posts-heading">
            <div>
              <p className="eyebrow">FROM YOUR DESK</p>
              <h2 id="posts-title">Your posts</h2>
            </div>
            <span className="post-count">{posts.length}</span>
          </div>

          {notice && <p className="notice-message" role="status">{notice}</p>}
          {error && <p className="error-message" role="alert">{error}</p>}

          {loading ? (
            <p className="empty-state">Loading your posts...</p>
          ) : posts.length === 0 ? (
            <div className="empty-state">
              <span className="empty-icon" aria-hidden="true">✳</span>
              <h3>No posts yet</h3>
              <p>Your next idea can start in the editor.</p>
            </div>
          ) : (
            <div className="post-list">
              {posts.map((post) => (
                <article className="post-card" key={post.id}>
                  <div className="post-card-top">
                    <span
                      className={`status-pill ${
                        post.status === "PB" ? "published" : "draft"
                      }`}
                    >
                      {post.status === "PB" ? "Published" : "Draft"}
                    </span>
                    <span className="post-date">{formatDate(post.publish)}</span>
                  </div>
                  <h3>{post.title}</h3>
                  <p className="post-slug">/{post.slug}</p>
                  <p className="post-body">{post.body}</p>
                  <div className="post-card-bottom">
                    <span className="author-name">
                      By {post.author_name || `author ${post.author}`}
                    </span>
                    <div className="post-actions">
                      <button
                        className="text-button"
                        onClick={() => editPost(post)}
                        type="button"
                      >
                        Edit
                      </button>
                      <button
                        className="text-button delete-button"
                        disabled={deletingId === post.id}
                        onClick={() => deletePost(post)}
                        type="button"
                      >
                        {deletingId === post.id ? "Deleting..." : "Delete"}
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
      <footer className="footer">Made for the love of a good sentence.</footer>
    </main>
  );
}
