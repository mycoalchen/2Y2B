// Home.js
import React, { useState } from 'react';

const App = () => {
  const [name, setName] = useState('[Your Name]');
  const [sources, setSources] = useState('[Source 1, Source 2]');
  const [topics, setTopics] = useState('[Topic 1, Topic 2]');
  const [topicList, setTopicList] = useState([]);

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleSourcesChange = (e) => {
    setSources(e.target.value);
  };

  const handleTopicsChange = (e) => {
    setTopics(e.target.value);
  };

  const handleTopicAdd = () => {
    if (topics.trim() !== '') {
      setTopicList([...topicList, topics.trim()]);
      setTopics('');
    }
  };

  const handleTopicRemove = (index) => {
    const updatedTopics = [...topicList];
    updatedTopics.splice(index, 1);
    setTopicList(updatedTopics);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    console.log('User preferences:', { name, sources, topics: topicList });
    // In a real app, you might want to handle the data or navigate to another page
  };

  return (
    <div className="app-container" style={{ backgroundColor: '#1E0B04', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: 'EB Garamond, serif' }}>
      <h1 style={{ color: '#fff', margin: '0', fontSize: '48px' }}>2Y2B</h1>
      <p style={{ color: '#fff', margin: '10px 0 20px', fontSize: '24px' }}>Your Yesterday Blended Briefly</p>
      <form onSubmit={handleSubmit} style={{ textAlign: 'center', color: '#fff' }}>
        <label>
          Name:
          <input type="text" value={name} onChange={handleNameChange} style={{ margin: '10px', padding: '8px', border: 'none', backgroundColor: '#1E0B04', width: '90px', fontSize: '16px' }} />
        </label>
        <br />
        <label>
          News Sources:
          <input type="text" value={sources} onChange={handleSourcesChange} style={{ margin: '10px', padding: '8px', border: 'none', backgroundColor: '#1E0B04', width: '145px', fontSize: '16px' }} />
        </label>
        <br />
        <label>
          Topics:
          <input type="text" value={topics} onChange={handleTopicsChange} style={{ margin: '10px', padding: '8px', border: 'none', backgroundColor: '#1E0B04', width: '120px', fontSize: '16px' }} />
        </label>
        <ul>
          {topicList.map((topic, index) => (
            <li key={index}>
              {topic}
              <button type="button" onClick={() => handleTopicRemove(index)} style = {{margin: '100px 0 20px'}}>
                Remove
              </button>
            </li>
          ))}
        </ul>
        <br />
        <button type="submit" style={{ padding: '10px', backgroundColor: '#1E0B04', color: '#fff', border: 'none', borderRadius: '0px', fontSize: '16px' }}>[Submit]</button>
      </form>
    </div>
  );
};

export default App;