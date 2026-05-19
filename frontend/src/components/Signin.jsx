import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

const Signin = () => {
  const navigate = useNavigate()

  const [formData, setFormData] = useState({
    username: "",
    password: ""
  })

  // 🔁 Auto redirect if already logged in
  useEffect(() => {
    const token = localStorage.getItem("token")
    if (token) {
      navigate("/promt")
    }
  }, [navigate])

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.username || !formData.password) {
      alert("Please fill all fields")
      return
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      })

      const data = await res.json()

      if (!res.ok) {
        alert(data.detail || "Login failed")
        return
      }

      // ✅ Save token
      localStorage.setItem("token", data.access_token)

      // ✅ Correct navigation (absolute path)
      navigate("/promt")

    } catch (err) {
      console.error(err)
      alert("Server error")
    }
  }

  return (
    <div>
      <form
        onSubmit={handleSubmit}
        style={{
          display: "grid",
          gap: "10px",
          width: "300px",
          margin: "auto"
        }}
      >
        <h2>Sign In</h2>

        <input
          type="text"
          name="username"
          placeholder="Enter username"
          value={formData.username}
          onChange={handleChange}
        />

        <input
          type="password"
          name="password"
          placeholder="Enter password"
          value={formData.password}
          onChange={handleChange}
        />

        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default Signin