import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";

const WellnessCheckIn = () => {
  const [user, setUser] = useState(null);
  const [survey, setSurvey] = useState({
    energy: 5,
    pain: 5,
    recovery: 5,
    mood: 5,
    expression: 5,
    calmness: 5,
    focus: 5,
    confidence: 5,
    challenge: 5,
    purpose: 5,
    values: 5,
    optimism: 5,
    support: 5,
    authenticity: 5,
    encouragement: 5,
    homeEnvironment: 5,
    surroundings: 5,
    community: 5,
  });
  const [history, setHistory] = useState([]);
  const [totalScore, setTotalScore] = useState(0);
  const [assessment, setAssessment] = useState("");

  useEffect(() => {
    const storedUser = localStorage.getItem("currentUser");
    if (storedUser) {
      setUser(storedUser);
      const storedData = localStorage.getItem(`wellnessHistory_${storedUser}`);
      if (storedData) {
        setHistory(JSON.parse(storedData));
      }
    }
  }, []);

  const handleLogin = () => {
    const username = prompt("Enter your username:");
    if (username) {
      setUser(username);
      localStorage.setItem("currentUser", username);
      const storedData = localStorage.getItem(`wellnessHistory_${username}`);
      if (storedData) {
        setHistory(JSON.parse(storedData));
      }
    }
  };

  const handleChange = (e) => {
    setSurvey({ ...survey, [e.target.name]: Number(e.target.value) });
  };

  const handleSubmit = () => {
    if (!user) {
      alert("Please log in first.");
      return;
    }
    const newEntry = { date: new Date().toLocaleDateString(), ...survey };
    const updatedHistory = [...history, newEntry];
    setHistory(updatedHistory);
    localStorage.setItem(`wellnessHistory_${user}`, JSON.stringify(updatedHistory));
    
    const score = Object.values(survey).reduce((acc, val) => acc + val, 0);
    setTotalScore(score);
    
    let result = "";
    if (score >= 144) {
      result = "Crushing it! Keep living this way, because it’s working beautifully.";
    } else if (score >= 117) {
      result = "Doing well! You might have some concerns, or consider making small changes.";
    } else if (score >= 90) {
      result = "Your lifestyle might be working in some areas, but struggling in others. Consider changes.";
    } else {
      result = "You have lots of room for growth. Any action you take will improve your deep health.";
    }
    setAssessment(result);
  };

  const pieData = Object.keys(survey).map((key) => ({ name: key, value: survey[key] }));
  const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#d88484", "#84d8d8", "#d8a384"];

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">Wellness Check-In</h1>
      {!user ? (
        <Button onClick={handleLogin}>Log In</Button>
      ) : (
        <>
          <p>Welcome, {user}!</p>
          <Card>
            <CardContent className="p-4 flex flex-col gap-4">
              {Object.keys(survey).map((key) => (
                <label key={key}>
                  {key.replace(/([A-Z])/g, ' $1').trim()} (1-10): 
                  <input 
                    type="number" 
                    name={key} 
                    value={survey[key]} 
                    onChange={handleChange} 
                    min="1" max="10" 
                  />
                </label>
              ))}
              <Button onClick={handleSubmit}>Submit Check-In</Button>
            </CardContent>
          </Card>
          {totalScore > 0 && (
            <div className="mt-4 p-4 border rounded-lg">
              <h2 className="text-lg font-bold">Total Score: {totalScore}</h2>
              <p>{assessment}</p>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100}>
                    {pieData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
          {history.length > 0 && (
            <div className="mt-6">
              <h2 className="text-lg font-bold">Progress Over Time</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={history}>
                  <XAxis dataKey="date" />
                  <YAxis domain={[1, 10]} />
                  <Tooltip />
                  {Object.keys(survey).map((key) => (
                    <Line key={key} type="monotone" dataKey={key} stroke="#8884d8" />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default WellnessCheckIn;
