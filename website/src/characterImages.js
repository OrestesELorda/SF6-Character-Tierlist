const characterImages = {
  "A.K.I.": "character_aki_l.png",
  "Alex": "character_alex_l.png",
  "Blanka": "character_blanka_l.png",
  "Cammy": "character_cammy_l.png",
  "Chun-Li": "character_chunli_l.png",
  "C. Viper": "character_cviper_l.png",
  "Dee Jay": "character_deejay_l.png",
  "Dhalsim": "character_dhalsim_l.png",
  "Ed": "character_ed_l.png",
  "Elena": "character_elena_l.png",
  "Akuma": "character_gouki_l.png",
  "Guile": "character_guile_l.png",
  "E. Honda": "character_honda_l.png",
  "Ingrid": "character_ingrid_l.png",
  "Jamie": "character_jamie_l.png",
  "JP": "character_jp_l.png",
  "Juri": "character_juri_l.png",
  "Ken": "character_ken_l.png",
  "Kimberly": "character_kimberly_l.png",
  "Lily": "character_lily_l.png",
  "Luke": "character_luke_l.png",
  "Mai": "character_mai_l.png",
  "Manon": "character_manon_l.png",
  "Marisa": "character_marisa_l.png",
  "Rashid": "character_rashid_l.png",
  "Ryu": "character_ryu_l.png",
  "Sagat": "character_sagat_l.png",
  "Terry": "character_terry_l.png",
  "M. Bison": "character_vega_l.png",
  "Yasmine": "character_yasmine_l.png",
  "Zangief": "character_zangief_l.png",
}

export function getCharacterImage(characterName) {
  const filename = characterImages[characterName]
  return filename ? `${import.meta.env.BASE_URL}characters/${filename}` : null
}

export default characterImages
