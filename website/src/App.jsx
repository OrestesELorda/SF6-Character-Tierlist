import rankings from './data/rankings.json'
import { getCharacterImage } from './characterImages'
import { getFlagImage } from './countryFlags'
import './App.css'

const TIERS = ['S', 'A', 'B', 'C', 'D', 'F']

function getLiquipediaUrl(playerName) {
  return `https://liquipedia.net/fighters/${playerName.replace(/ /g, '_')}`
}

function PlayerCard({ entry }) {
  const flagSrc = getFlagImage(entry.flag)
  return (
    <a
      className="player-card"
      href={getLiquipediaUrl(entry.player)}
      target="_blank"
      rel="noreferrer"
    >
      <div className="player-characters">
        {entry.characters.map(character => {
          const imageSrc = getCharacterImage(character)
          return imageSrc ? (
            <img key={character} src={imageSrc} alt={character} title={character} />
          ) : null
        })}
      </div>
      <div className="player-info">
        {flagSrc ? (
          <img className="player-flag" src={flagSrc} alt={entry.flag} title={entry.flag} />
        ) : null}
        <span className="player-name">{entry.player}</span>
      </div>
    </a>
  )
}

function App() {
  const playersByTier = {}
  for (const tier of TIERS) {
    playersByTier[tier] = []
  }
  for (const entry of rankings) {
    playersByTier[entry.tier].push(entry)
  }

  return (
    <div className="tierlist-page">
      <h1>Street fighter 6 2026 Season Rank</h1>
      <div className="tierlist">
        {TIERS.map(tier => (
          <div className="tier-row" key={tier}>
            <div className={`tier-label tier-${tier}`}>{tier}</div>
            <div className="tier-players">
              {playersByTier[tier].map(entry => (
                <PlayerCard key={entry.player} entry={entry} />
              ))}
            </div>
          </div>
        ))}
      </div>
      <p className="attribution">
        Data from{' '}
        <a href="https://liquipedia.net/fighters/" target="_blank" rel="noreferrer">
          Liquipedia
        </a>
        , licensed under CC-BY-SA
      </p>
    </div>
  )
}

export default App
