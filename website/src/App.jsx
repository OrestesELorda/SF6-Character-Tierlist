import rankings from './data/rankings.json'

function App() {
  return (
    <div>
      <h1>SF6 Player Rankings</h1>
      <ol>
        {rankings.map(entry => (
          <li key={entry.player}>
            {entry.player} — score: {entry.score.toFixed(2)}
          </li>
        ))}
      </ol>
    </div>
  )
}

export default App
