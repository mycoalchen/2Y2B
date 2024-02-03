// Home.js
import React, { useState } from 'react';

const App = () => {
  const [name, setName] = useState('[Your Name]');
  const [sources, setSources] = useState('[Source 1, Source 2]');
  const [topics, setTopics] = useState('[Topic 1, Topic 2]');

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleSourcesChange = (e) => {
    setSources(e.target.value);
  };

  const handleTopicsChange = (e) => {
    setTopics(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    console.log('User preferences:', { name, sources, topics: topics });

    fetch(`/submit?name=${name}&sources=${sources}&topics=${topics}`).then(res => res.json()).then(data => {
      console.log(data)
    })
  };

  const offWhite1 = "#F6F1Ed";
  const offWhite2 = "#C5BaB6";
  const coffee = "#1E0B04"

  return (
    <div className="app-container" style={{ backgroundColor: coffee, height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: 'EB Garamond, serif' }}>

      <p style={{ color: offWhite1, margin: '0', fontSize: '48px' }}>2Y2B</p>

      <form onSubmit={handleSubmit} style={{ textAlign: 'center', color: offWhite1 }}>
        <label>
          <input type="text" value={name} onChange={handleNameChange} style={{ margin: '10px', padding: '8px', border: 'none', backgroundColor: '#00000000', width: '90px', fontSize: '16px', outline: 'none', caretColor: 'auto', color: offWhite1 }} placeholder="[Your name]" />
        </label>
        <br />
        <label>
          News Sources:
          <input type="text" value={sources} onChange={handleSourcesChange} style={{ margin: '10px', padding: '8px', border: 'none', backgroundColor: '#00000000', width: '145px', fontSize: '16px' }} />
        </label>
        <br />
        <label>
          Topics:
          <input type="text" value={topics} onChange={handleTopicsChange} style={{ margin: '10px', padding: '8px', border: 'none', backgroundColor: '#00000000', width: '120px', fontSize: '16px' }} />
        </label>

        <br />
        <button type="submit" style={{ padding: '10px', backgroundColor: '#00000000', color: offWhite1, border: 'none', borderRadius: '0px', fontSize: '18px', fontWeight: 'normal', transition: 'font-weight 0.3s', fontFamily: 'EB Garamond' }} onMouseOver={(e) => e.target.style.fontWeight = 'bold'} onMouseOut={(e) => e.target.style.fontWeight = 'normal'}>{`[Submit]`}</button>
      </form>
    </div>
  );
};

export default App;