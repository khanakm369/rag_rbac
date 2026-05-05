import React, { useEffect, useState } from "react"

const Profile = () => {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem("token")

      if (!token) return

      const res = await fetch("http://127.0.0.1:8000/profile", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      const data = await res.json()
      setUser(data)
    }

    fetchProfile()
  }, [])

  return (
    <div>
      <h2>Profile</h2>
      {user ? (
        <>
          <p>{user.message}</p>
          <p>Role: {user.role}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  )
}

export default Profile