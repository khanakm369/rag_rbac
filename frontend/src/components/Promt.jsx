import React, { useState } from 'react'

const Promt = () => {
  const [query, setQuery] = useState("")
  const [response, setResponse] = useState("")

  const handleSubmit = async () => {
    if (!query) {
      alert("Please enter a question")
      return
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
          question: query
        })
      })

      const data = await res.json()
      setResponse(data.answer)

    } catch (err) {
      console.error(err)
      alert("Error connecting to backend")
    }
  }

  return (
    <div>
      <h2>Prompt</h2>

      <input
        type='text'
        placeholder='Ask your Question'
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={handleSubmit}>Send</button>

      {response && (
        <p><strong>Response:</strong> {response}</p>
      )}
    </div>
  )
}

export default Promt