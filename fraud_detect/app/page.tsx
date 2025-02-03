"use client";

import { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera } from "@react-three/drei";
import { Globe } from "@/components/3d/globe";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Search, Send, Share2, AlertTriangle, BarChart } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Progress } from "@/components/ui/progress";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import axios from 'axios';





export default function Home() {
  const [articleUrl, setArticleUrl] = useState("");
  const [chatMessage, setChatMessage] = useState("");
  const [userQuery, setUserQuery] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [credibilityScore, setCredibilityScore] = useState<number >(0);
  const [reliabilityScore, setReliabilityScore] = useState<number >(0);
  const [noQuery, setNoQuery] = useState(true);
  const [gptResponse, setGptResponse] = useState('');

  
  const [chatMessages, setChatMessages] = useState<Array<{
    role: "user" | "assistant";
    content: string;
  }>>([]);

  const handleAnalyzeArticle = async () => {
    setIsAnalyzing(true);
    try {
      // Send the article URL to the backend for processing
      const response = await axios.post('http://localhost:5000/process', {
        article_link: articleUrl,
      });

      // Assuming the response contains the collected data as integers
      const { credibilityScore, reliabilityScore } = response.data;
      setNoQuery(false);
      // Update the state with the analysis result
      setCredibilityScore(credibilityScore);
      setReliabilityScore(reliabilityScore);
      console.log(credibilityScore, reliabilityScore);
    } catch (error) {
      console.error('Error analyzing article:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatMessage.trim()) return;
  
    // Display the user's message in the chat
    setChatMessages([...chatMessages, { role: "user", content: chatMessage }]);
    const currentMessage = chatMessage;
    setChatMessage("");
  
    try {
      // Send the user's message to the backend
      const response = await axios.post('http://localhost:5000/chat', {
        input_query: currentMessage,
      });
  
      // Assuming the backend returns the AI's response in 'response.data'
      const aiResponse = response.data;
  
      // Display the AI's response in the chat
      setChatMessages(prev => [...prev, { role: "assistant", content: aiResponse }]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Optionally, display an error message in the chat
      setChatMessages(prev => [...prev, { role: "assistant", content: "Sorry, there was an error processing your request." }]);
    }
  };
  
  

  const pieChartData = credibilityScore ? [
    { name: "Factual", value: reliabilityScore },
    { name: "Non-Factual", value: 100 - reliabilityScore },
  ] : [];

  const COLORS = ["#4f46e5", "#e11d48"];

  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-secondary">
      <div className="fixed inset-0 -z-10">
        <Canvas>
          <PerspectiveCamera makeDefault position={[0, 0, 5]} />
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Globe />
          <OrbitControls enableZoom={false} enablePan={false} />
        </Canvas>
      </div>
  
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center justify-center min-h-[80vh] space-y-8"
        >
          {/* Title with Glowing Animation */}
          <h1 className="text-4xl md:text-6xl font-bold text-center bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary-foreground animate-glow">
            AI Fact Checker
          </h1>
  
          <Card className="w-full max-w-4xl p-6 backdrop-blur-lg bg-background/80">
            <div className="space-y-6">
              {/* Article URL Input */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Article URL</label>
                <div className="flex space-x-2">
                  <Input
                    type="url"
                    placeholder="Paste article URL to verify..."
                    value={articleUrl}
                    onChange={(e) => setArticleUrl(e.target.value)}
                    className="flex-1"
                  />
                  <Button onClick={handleAnalyzeArticle} disabled={isAnalyzing}>
                    <Search className="h-5 w-5 mr-2" />
                    Analyze
                  </Button>
                </div>
              </div>
              {isAnalyzing && <p className="loader">Analyzing article...</p>}
              {/* Analysis Results */}
              <AnimatePresence>
                {noQuery===false && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="space-y-6"
                  >
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-4">
                        <h3 className="text-lg font-semibold">Analysis Results</h3>
                        <div className="space-y-4">
                          <div>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm">Credibility Score</span>
                              <span className="text-sm font-medium">
                                {credibilityScore}%
                              </span>
                            </div>
                            <Progress
                              value={credibilityScore}
                            />
                          </div>
                          <div>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm">Source Reliability</span>
                              <span className="text-sm font-medium">
                                {reliabilityScore}%
                              </span>
                            </div>
                            <Progress
                              value={reliabilityScore}
                            />
                          </div>
                        </div>
                      </div>
  
                      <div className="h-[200px]">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={pieChartData}
                              cx="50%"
                              cy="50%"
                              innerRadius={60}
                              outerRadius={80}
                              fill="#8884d8"
                              paddingAngle={5}
                              dataKey="value"
                            >
                              {pieChartData.map((entry, index) => (
                                <Cell
                                  key={`cell-${index}`}
                                  fill={COLORS[index % COLORS.length]}
                                />
                              ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
  
                    {/* Chat Interface */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold">
                        Ask Questions About the Article
                      </h3>
                      <div className="h-[200px] overflow-y-auto border rounded-lg p-4 space-y-4">
                        {chatMessages.map((message, index) => (
                          <div
                            key={index}
                            className={`flex ${
                              message.role === "user"
                                ? "justify-end"
                                : "justify-start"
                            }`}
                          >
                            <div
                              className={`max-w-[80%] rounded-lg p-3 ${
                                message.role === "user"
                                  ? "bg-primary text-primary-foreground"
                                  : "bg-muted"
                              }`}
                            >
                              {message.content}
                            </div>
                          </div>
                        ))}
                      </div>
                      <div className="flex space-x-2">
                        <Textarea
                          placeholder="Ask a question about the article..."
                          value={chatMessage}
                          onChange={(e) => setChatMessage(e.target.value)}
                          className="flex-1"
                        />
                        <Button onClick={handleSendMessage}>
                          <Send className="h-5 w-5" />
                        </Button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
  
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="flex items-center justify-between text-sm text-muted-foreground"
              >
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="h-4 w-4" />
                  <span>Verify sources before sharing</span>
                </div>
              </motion.div>
            </div>
          </Card>
        </motion.div>
      </div>
    </main>
  );
  
  
  
}