// Home.js
import React, { useState } from 'react';

const App = () => {
  const [name, setName] = useState('[Your Name]');
  const [selectedSources, setSelectedSources] = useState([]);
  const [topics, setTopics] = useState('[Topic 1, Topic 2, Topic 3]');
  const [suggestedSources] = useState(['CNN', 'BBC', 'Reuters', 'The New York Times']);
  const [topicList, setTopicList] = useState([]);

  const handleNameChange = (e) => {
    setName(e.target.value);
    /*const inputValue = e.target.value;
  if (inputValue.startsWith('[') && inputValue.endsWith(']')) {
    setName(inputValue);
  } else {
    setName(`[${inputValue}]`);
  }*/
  }
  
  const handleSourcesChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions, (option) => option.value);
    setSelectedSources(selectedOptions);
  };

  const handleTopicsChange = (e) => {
    const inputValue = e.target.value;
    setTopics(inputValue);
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

    console.log('User preferences:', { name, selectedSources, topics: topicList });
    // In a real app, you might want to handle the data or navigate to another page
  };

  return (
    <div className="app-container" style={{ backgroundColor: '#1E0B04', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: 'EB Garamond, serif' }}>
      <h1 style={{ color: '#fff', marginBottom: '6px', fontSize: '48px' }}>2Y2B</h1>
      <h2 style={{ color: '#fff', marginTop: '0', marginBottom: '20px' , fontSize: '24px'}}>Your Yesterday Blended Briefly</h2>
      <form onSubmit={handleSubmit} style={{ textAlign: 'center', color: '#fff' }}>
        <label>
          Name:
          <input type="text" value={name} onChange={handleNameChange} style={{ margin: '10px', border: 'none', backgroundColor: '#1E0B04' }} />
        </label>
        <br />
        <label>
          News Sources (Select multiple):
          <select multiple value={selectedSources} onChange={handleSourcesChange} style={{ margin: '10px' }}>
            {suggestedSources.map((source) => (
              <option key={source} value={source}>
                {source}
              </option>
            ))}
          </select>
        </label>
        <br />
        <label>
          Topics:
          <input type="text" value={topics} onChange={handleTopicsChange} style={{ margin: '10px', border: 'none', backgroundColor: '#1E0B04' }} />
          <button type="button" onClick={handleTopicAdd}>
            Add Topic
          </button>
        </label>
        <ul>
          {topicList.map((topic, index) => (
            <li key={index}>
              {topic}
              <button type="button" onClick={() => handleTopicRemove(index)}>
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