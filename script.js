async function loadChromas() {
  const response = await fetch('data/chromas.json');
  const chromas = await response.json();
  displayChromas(chromas);

  document.getElementById('search').addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = chromas.filter(c =>
      c.champion.toLowerCase().includes(term) ||
      c.skin.toLowerCase().includes(term)
    );
    displayChromas(filtered);
  });
}

function displayChromas(chromas) {
  const container = document.getElementById('chroma-list');
  container.innerHTML = chromas.map(c => `
    <div class="chroma-card">
      <img src="${c.image}" alt="${c.name}" loading="lazy">
      <div>
        <strong>${c.champion}</strong> – ${c.skin}<br>
        <small>${c.name}</small>
      </div>
    </div>
  `).join('');
}

loadChromas();