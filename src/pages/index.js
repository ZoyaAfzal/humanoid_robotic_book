import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  // Chapter data with lessons
  const chapters = [
    {
      number: 1,
      title: "Spec-Kit Plus & Robotics Foundation",
      description: "Learn the fundamentals of humanoid robotics and the Spec-Kit Plus platform.",
      link: "/docs/chapter1/",
      color: "linear-gradient(135deg, #1a5fb4 0%, #154e92 100%)", // Blue for foundations
      lessons: [
        { title: "Spec-Kit Plus Workflow", link: "/docs/chapter1/lesson1/spec-kit-plus-workflow" },
        { title: "Physical AI & Embodied Intelligence", link: "/docs/chapter1/lesson2/physical-ai-embodied-intelligence" },
        { title: "Development Environment Setup", link: "/docs/chapter1/lesson3/development-environment-setup" }
      ]
    },
    {
      number: 2,
      title: "The Robotic Nervous System (ROS 2)",
      description: "Explore ROS 2 architecture and how it serves as the nervous system for robots.",
      link: "/docs/chapter2/",
      color: "linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%)", // Purple for systems
      lessons: [
        { title: "ROS 2 Architecture (Nodes, Topics, Services)", link: "/docs/chapter2/lesson1/ros2-architecture" },
        { title: "Modeling the Humanoid Robot (URDF)", link: "/docs/chapter2/lesson2/humanoid-robot-modeling" },
        { title: "Bridging AI Agents (rclpy)", link: "/docs/chapter2/lesson3/bridging-ai-agents" }
      ]
    },
    {
      number: 3,
      title: "The Digital Twin (Simulation)",
      description: "Understand digital twin technology and simulation environments.",
      link: "/docs/chapter3/",
      color: "linear-gradient(135deg, #fd7e14 0%, #e06c0c 100%)", // Orange for simulation
      lessons: [
        { title: "Gazebo Environment Setup", link: "/docs/chapter3/lesson1/gazebo-environment-setup" },
        { title: "Simulating Physics & Collisions", link: "/docs/chapter3/lesson2/simulating-physics-collisions" },
        { title: "Sensor Simulation (LiDAR/IMU)", link: "/docs/chapter3/lesson3/sensor-simulation" }
      ]
    },
    {
      number: 4,
      title: "The AI-Robot Brain (NVIDIA Isaac™)",
      description: "Discover AI integration and the NVIDIA Isaac platform for robot brains.",
      link: "/docs/chapter4/",
      color: "linear-gradient(135deg, #28a745 0%, #218838 100%)", // Green for AI/brain
      lessons: [
        { title: "Isaac Sim & Synthetic Data", link: "/docs/chapter4/lesson1/isaac-sim-synthetic-data" },
        { title: "Hardware-Accelerated Navigation (Isaac ROS)", link: "/docs/chapter4/lesson2/hardware-accelerated-navigation" },
        { title: "Bipedal Path Planning (Nav2)", link: "/docs/chapter4/lesson3/bipedal-path-planning" }
      ]
    },
    {
      number: 5,
      title: "Vision-Language-Action (VLA) & Capstone",
      description: "Master Vision-Language-Action systems and complete your capstone project.",
      link: "/docs/chapter5/",
      color: "linear-gradient(135deg, #e83e8c 0%, #d22572 100%)", // Pink for advanced concepts
      lessons: [
        { title: "Voice-to-Action (Whisper Integration)", link: "/docs/chapter5/lesson1/voice-to-action" },
        { title: "Cognitive Planning (LLM to ROS Action Sequence)", link: "/docs/chapter5/lesson2/cognitive-planning" },
        { title: "Capstone Project Execution", link: "/docs/chapter5/lesson3/capstone-project-execution" }
      ]
    }
  ];

  // Features data
  const features = [
    {
      title: "🤖 Humanoid Robotics",
      description: "Master the fundamentals of building and controlling humanoid robots"
    },
    {
      title: "🧠 AI Integration",
      description: "Learn how to integrate artificial intelligence with robotic systems"
    },
    {
      title: "🛠️ Practical Skills",
      description: "Gain hands-on experience with real robotics platforms and tools"
    },
    {
      title: "🏗️ Industry Standards",
      description: "Learn industry-standard tools and frameworks used in robotics"
    }
  ];

  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Comprehensive guide to humanoid robotics">
      <main>
        {/* Hero Section - Professional */}
        <section className="hero hero--primary" style={{
          padding: '8rem 2rem',
          textAlign: 'center',
          background: 'linear-gradient(160deg, #1a5f3c 0%, #28a745 30%, #218838 100%)',
          color: 'white',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'url("data:image/svg+xml,%3Csvg width=\'100\' height=\'100\' viewBox=\'0 0 100 100\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cdefs%3E%3ClinearGradient id=\'a\' x1=\'0%25\' y1=\'0%25\' x2=\'100%25\' y2=\'100%25\'%3E%3Cstop offset=\'0%25\' stop-color=\'%23ffffff\' stop-opacity=\'0.08\'/%3E%3Cstop offset=\'100%25\' stop-color=\'%23ffffff\' stop-opacity=\'0.02\'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath fill=\'none\' d=\'M33.3,0 L66.6,0 L100,33.3 L100,66.6 L66.6,100 L33.3,100 L0,66.6 L0,33.3 Z\' fill=\'url(%23a)\'/%3E%3C/svg%3E")',
            opacity: 0.15,
            backgroundSize: '120px'
          }}></div>

          <div style={{position: 'relative', zIndex: 1, maxWidth: '1000px', margin: '0 auto'}}>
            <Heading as="h1" style={{
              fontSize: '3.5rem',
              fontWeight: '800',
              marginBottom: '1.5rem',
              textShadow: '0 4px 12px rgba(0,0,0,0.3)',
              textAlign: 'center',
              letterSpacing: '-0.02em',
              lineHeight: '1.2',
              animation: 'fadeInUp 1s ease-out',
              opacity: 1,  // Always ensure visibility
              transform: 'translateY(0px)',  // Start at final position
              // Remove animationFillMode to prevent any issues
            }}>
              {siteConfig.title}
            </Heading>

            <p style={{
              fontSize: '1.6rem',
              maxWidth: '800px',
              margin: '0 auto 1.5rem',
              textShadow: '0 2px 4px rgba(0,0,0,0.3)',
              textAlign: 'center',
              lineHeight: '1.6',
              color: 'rgba(255, 255, 255, 0.95)',
              animation: 'fadeInUp 1s ease-out 0.2s',
              opacity: 1,  // Always ensure visibility
              transform: 'translateY(0px)',  // Start at final position
              // Remove animationFillMode to prevent any issues
            }}>
              {siteConfig.tagline}
            </p>

            {/* Detailed Book Introduction */}
            <div style={{
              fontSize: '1.2rem',
              maxWidth: '800px',
              margin: '0 auto 2.5rem',
              textShadow: '0 2px 4px rgba(0,0,0,0.3)',
              textAlign: 'center',
              lineHeight: '1.7',
              color: 'rgba(255, 255, 255, 0.9)',
              animation: 'fadeInUp 1s ease-out 0.4s',
              opacity: 1,  // Always ensure visibility
              transform: 'translateY(0px)',  // Start at final position
              // Remove animationFillMode to prevent any issues
            }}>
              <p>
                This comprehensive guide takes you from robotics fundamentals to advanced AI integration,
                covering everything from ROS 2 architecture to NVIDIA Isaac platforms.
              </p>
              <p style={{marginTop: '0.75rem'}}>
                Master humanoid robotics development through hands-on projects, industry-standard tools,
                and cutting-edge Vision-Language-Action systems.
              </p>
            </div>

            <div style={{
              margin: '2.5rem 0',
              textAlign: 'center'
            }}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro"
                style={{
                  margin: '0 0.75rem 1rem 0.75rem',
                  fontSize: '1.2rem',
                  padding: '1.1rem 2.5rem',
                  borderRadius: '12px',
                  boxShadow: '0 6px 20px rgba(0,0,0,0.25)',
                  fontWeight: '600',
                  transition: 'all 0.3s ease',
                  background: 'white',
                  color: '#28a745'
                }}
                onMouseEnter={(e) => {
                  e.target.style.transform = 'translateY(-3px)';
                  e.target.style.boxShadow = '0 10px 25px rgba(0,0,0,0.3)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = '0 6px 20px rgba(0,0,0,0.25)';
                }}
              >
                Start Learning
              </Link>
              <Link
                className="button button--outline button--lg"
                to="/docs/intro"
                style={{
                  margin: '0 0.75rem 1rem 0.75rem',
                  fontSize: '1.2rem',
                  padding: '1.1rem 2.5rem',
                  color: 'white',
                  borderColor: 'rgba(255, 255, 255, 0.8)',
                  borderRadius: '12px',
                  boxShadow: '0 6px 20px rgba(0,0,0,0.2)',
                  fontWeight: '600',
                  transition: 'all 0.3s ease',
                  background: 'transparent'
                }}
                onMouseEnter={(e) => {
                  e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                  e.target.style.borderColor = 'white';
                  e.target.style.transform = 'translateY(-3px)';
                  e.target.style.boxShadow = '0 10px 25px rgba(0,0,0,0.25)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.backgroundColor = 'transparent';
                  e.target.style.borderColor = 'rgba(255, 255, 255, 0.8)';
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = '0 6px 20px rgba(0,0,0,0.2)';
                }}
              >
                Browse Content
              </Link>
            </div>

            <div style={{
              display: 'flex',
              justifyContent: 'center',
              gap: '2rem',
              marginTop: '3rem',
              flexWrap: 'wrap'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                color: 'rgba(255, 255, 255, 0.9)',
                fontSize: '1.1rem'
              }}>
                <span style={{marginRight: '0.75rem', fontSize: '1.5rem'}}>🎓</span>
                Comprehensive Curriculum
              </div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                color: 'rgba(255, 255, 255, 0.9)',
                fontSize: '1.1rem'
              }}>
                <span style={{marginRight: '0.75rem', fontSize: '1.5rem'}}>🚀</span>
                Hands-on Projects
              </div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                color: 'rgba(255, 255, 255, 0.9)',
                fontSize: '1.1rem'
              }}>
                <span style={{marginRight: '0.75rem', fontSize: '1.5rem'}}>🔧</span>
                Industry Tools
              </div>
            </div>
          </div>
        </section>

        {/* Chapter Components Section - Professional */}
        <section style={{
          padding: '6rem 2rem',
          backgroundColor: '#ffffff',
          position: 'relative'
        }}>
          <div className="container">
            <div style={{
              textAlign: 'center',
              marginBottom: '4rem'
            }}>
              <Heading as="h2" style={{
                fontSize: '2.5rem',
                marginBottom: '1rem',
                color: '#28a745',
                textAlign: 'center'
              }}>
                Course Chapters
              </Heading>
              <p style={{fontSize: '1.2rem', color: '#666', maxWidth: '600px', margin: '1rem auto 0', textAlign: 'center'}}>
                Explore comprehensive chapters designed to take you from beginner to expert
              </p>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '1.5rem',
              marginTop: '2rem'
            }}>
              {chapters.map((chapter, index) => (
                <div
                  key={index}
                  className="card"
                  style={{
                    padding: '0',
                    transition: 'all 0.3s ease',
                    border: 'none',
                    borderRadius: '12px',
                    background: 'white',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
                    minHeight: '320px',
                    overflow: 'hidden',
                    position: 'relative'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-5px)';
                    e.currentTarget.style.boxShadow = '0 12px 30px rgba(26, 95, 180, 0.15)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
                  }}
                >
                  {/* Chapter header with gradient */}
                  <div style={{
                    background: chapter.color,
                    padding: '1.5rem 1.5rem 1rem',
                    color: 'white',
                    textAlign: 'center'
                  }}>
                    <div style={{
                      fontSize: '2.5rem',
                      fontWeight: 'bold',
                      marginBottom: '0.5rem',
                      textShadow: '0 2px 4px rgba(0,0,0,0.3)'
                    }}>
                      {chapter.number}
                    </div>
                    <Heading as="h3" style={{
                      fontSize: '1.3rem',
                      marginBottom: '0.5rem',
                      color: 'white',
                      textShadow: '0 1px 2px rgba(0,0,0,0.3)'
                    }}>
                      {chapter.title}
                    </Heading>
                  </div>

                  {/* Chapter content */}
                  <div style={{
                    padding: '1.5rem',
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%'
                  }}>
                    <div style={{flex: 1}}>
                      <p style={{
                        marginBottom: '1.25rem',
                        color: '#666',
                        lineHeight: '1.5',
                        fontSize: '0.9rem',
                        minHeight: '60px'
                      }}>
                        {chapter.description}
                      </p>

                      <div style={{
                        marginBottom: '1.25rem'
                      }}>
                        <h4 style={{
                          color: chapter.color.includes('#1a5fb4') ? '#1a5fb4' :
                                 chapter.color.includes('#6f42c1') ? '#6f42c1' :
                                 chapter.color.includes('#fd7e14') ? '#fd7e14' :
                                 chapter.color.includes('#28a745') ? '#28a745' :
                                 chapter.color.includes('#e83e8c') ? '#e83e8c' : '#28a745',
                          marginBottom: '0.5rem',
                          fontSize: '0.95rem',
                          fontWeight: '600'
                        }}>
                          Lessons:
                        </h4>
                        <ul style={{
                          listStyle: 'none',
                          padding: 0,
                          margin: 0
                        }}>
                          {chapter.lessons.map((lesson, lessonIndex) => (
                            <li key={lessonIndex} style={{
                              marginBottom: '0.25rem',
                              fontSize: '0.85rem'
                            }}>
                              <Link
                                to={lesson.link}
                                style={{
                                  color: '#28a745',
                                  textDecoration: 'none',
                                  fontWeight: '500',
                                  padding: '0.25rem 0',
                                  display: 'block',
                                  borderRadius: '4px',
                                  transition: 'background-color 0.2s ease'
                                }}
                                onMouseEnter={(e) => {
                                  e.target.style.backgroundColor = 'rgba(40, 167, 69, 0.05)';
                                }}
                                onMouseLeave={(e) => {
                                  e.target.style.backgroundColor = 'transparent';
                                }}
                              >
                                • {lesson.title}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div style={{
                      textAlign: 'center',
                      marginTop: 'auto'
                    }}>
                      <Link
                        className="button button--primary"
                        to={chapter.link}
                        style={{
                          textDecoration: 'none',
                          borderRadius: '25px',
                          padding: '0.6rem 1.2rem',
                          fontSize: '0.85rem',
                          background: 'linear-gradient(135deg, #28a745 0%, #218838 100%)',
                          color: 'white',
                          border: 'none',
                          fontWeight: '500',
                          boxShadow: '0 4px 15px rgba(40, 167, 69, 0.2)'
                        }}
                      >
                        Explore Chapter
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Professional Features Section */}
        <section style={{padding: '6rem 2rem', backgroundColor: '#f8f9fa'}}>
          <div className="container">
            <div style={{
              textAlign: 'center',
              marginBottom: '4rem'
            }}>
              <Heading as="h2" style={{
                fontSize: '2.5rem',
                marginBottom: '1rem',
                color: '#28a745',
                textAlign: 'center'
              }}>
                What You'll Master
              </Heading>
              <p style={{fontSize: '1.2rem', color: '#666', maxWidth: '600px', margin: '1rem auto 0', textAlign: 'center'}}>
                Comprehensive skills to excel in humanoid robotics development
              </p>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '1.5rem'
            }}>
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="card"
                  style={{
                    padding: '0',
                    transition: 'all 0.3s ease',
                    border: 'none',
                    borderRadius: '12px',
                    background: 'white',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
                    minHeight: '320px', /* Match chapter card height */
                    overflow: 'hidden',
                    position: 'relative'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-5px)';
                    e.currentTarget.style.boxShadow = '0 12px 30px rgba(26, 95, 180, 0.15)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
                  }}
                >
                  {/* Feature header with gradient - using theme-appropriate colors */}
                  <div style={{
                    background: index === 0 ? 'linear-gradient(135deg, #1a5fb4 0%, #154e92 100%)' :  // Blue for first feature
                               index === 1 ? 'linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%)' :  // Purple for second feature
                               index === 2 ? 'linear-gradient(135deg, #fd7e14 0%, #e06c0c 100%)' :  // Orange for third feature
                               index === 3 ? 'linear-gradient(135deg, #e83e8c 0%, #d22572 100%)' :  // Pink for fourth feature
                               'linear-gradient(135deg, #28a745 0%, #218838 100%)',               // Green for others
                    padding: '1.5rem',
                    color: 'white',
                    textAlign: 'center'
                  }}>
                    <Heading as="h3" style={{
                      fontSize: '1.3rem',
                      marginBottom: '0.5rem',
                      color: 'white',
                      textShadow: '0 1px 2px rgba(0,0,0,0.3)'
                    }}>
                      {feature.title}
                    </Heading>
                  </div>

                  {/* Feature content - match chapter layout */}
                  <div style={{
                    padding: '1.5rem',
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%'
                  }}>
                    <div style={{flex: 1}}>
                      <p style={{
                        marginBottom: '1.25rem',
                        color: '#666',
                        lineHeight: '1.5',
                        fontSize: '0.9rem',
                        minHeight: '60px'
                      }}>
                        {feature.description}
                      </p>
                    </div>

                    <div style={{
                      textAlign: 'center',
                      marginTop: 'auto'
                    }}>
                      <div
                        style={{
                          textDecoration: 'none',
                          borderRadius: '25px',
                          padding: '0.6rem 1.2rem',
                          fontSize: '0.85rem',
                          background: index === 0 ? 'linear-gradient(135deg, #1a5fb4 0%, #154e92 100%)' :  // Blue for first feature
                                     index === 1 ? 'linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%)' :  // Purple for second feature
                                     index === 2 ? 'linear-gradient(135deg, #fd7e14 0%, #e06c0c 100%)' :  // Orange for third feature
                                     index === 3 ? 'linear-gradient(135deg, #e83e8c 0%, #d22572 100%)' :  // Pink for fourth feature
                                     'linear-gradient(135deg, #28a745 0%, #218838 100%)',               // Green for others
                          color: 'white',
                          border: 'none',
                          fontWeight: '500',
                          boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                          cursor: 'default',
                          opacity: 0.7
                        }}
                      >
                        Learn More
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Professional CTA Section */}
        <section style={{
          padding: '4rem 2rem',
          background: 'linear-gradient(135deg, #28a745 0%, #218838 100%)',
          textAlign: 'center',
          color: 'white'
        }}>
          <div className="container">
            <Heading as="h2" style={{
              fontSize: '2.5rem',
              marginBottom: '1rem'
            }}>
              Ready to Start Your Journey?
            </Heading>
            <p style={{
              fontSize: '1.2rem',
              marginBottom: '2rem',
              maxWidth: '600px',
              margin: '0 auto 2rem'
            }}>
              Join thousands of learners mastering humanoid robotics with our comprehensive curriculum.
            </p>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro"
              style={{
                fontSize: '1.2rem',
                padding: '1rem 3rem',
                borderRadius: '8px'
              }}
            >
              Begin Learning Today
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
