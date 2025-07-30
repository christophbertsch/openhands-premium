"""
Enhanced Quality Agents for OpenHands
These agents are optimized for production-grade performance and quality
"""

from typing import Dict, Any, List, Optional
from openhands.agenthub.codeact_agent.codeact_agent import CodeActAgent
from openhands.core.config import AgentConfig
from openhands.core.message import Message
from openhands.events.action import Action
from openhands.events.observation import Observation


class PremiumCodeActAgent(CodeActAgent):
    """
    Enhanced CodeAct agent with premium quality features:
    - Advanced reasoning capabilities
    - Comprehensive error handling
    - Quality-focused code generation
    - Enhanced debugging and testing
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.quality_mode = True
        self.max_quality_iterations = 3
        
    def get_system_message(self) -> str:
        """Enhanced system message for premium quality"""
        return """You are an elite software engineer and AI assistant with world-class expertise in:

🎯 CORE COMPETENCIES:
- Advanced software architecture and design patterns
- Production-grade code development and optimization
- Comprehensive testing strategies and debugging
- Security-first development practices
- Performance optimization and scalability
- DevOps and deployment best practices

🔧 TECHNICAL EXCELLENCE:
- Write clean, maintainable, and efficient code
- Follow industry best practices and coding standards
- Implement comprehensive error handling and validation
- Create thorough documentation and comments
- Design scalable and robust solutions
- Optimize for performance and resource efficiency

🛡️ QUALITY ASSURANCE:
- Always validate inputs and handle edge cases
- Implement proper logging and monitoring
- Write comprehensive tests (unit, integration, e2e)
- Consider security implications in every decision
- Follow SOLID principles and clean architecture
- Ensure code is production-ready

🚀 PROBLEM-SOLVING APPROACH:
1. Thoroughly analyze requirements and constraints
2. Design elegant and scalable solutions
3. Break complex problems into manageable components
4. Implement with attention to detail and quality
5. Test comprehensively and handle edge cases
6. Document clearly and provide usage examples
7. Optimize for maintainability and extensibility

🎨 CODE QUALITY STANDARDS:
- Use meaningful names for variables, functions, and classes
- Keep functions small and focused (single responsibility)
- Avoid code duplication (DRY principle)
- Write self-documenting code with clear logic flow
- Include comprehensive docstrings and comments
- Follow language-specific style guides (PEP 8, etc.)

🔍 DEBUGGING AND TESTING:
- Use systematic debugging approaches
- Write tests that cover normal, edge, and error cases
- Implement proper logging for troubleshooting
- Use appropriate debugging tools and techniques
- Validate solutions thoroughly before delivery

Remember: Quality is not negotiable. Every solution should be production-ready, secure, and maintainable."""

    def step(self, state) -> Action:
        """Enhanced step with quality checks"""
        # Perform quality pre-checks
        if self.quality_mode:
            self._perform_quality_checks(state)
        
        # Execute the standard step
        action = super().step(state)
        
        # Perform quality post-checks
        if self.quality_mode:
            action = self._enhance_action_quality(action, state)
        
        return action
    
    def _perform_quality_checks(self, state) -> None:
        """Perform quality checks before taking action"""
        # Check for common issues in the current state
        if hasattr(state, 'latest_observation'):
            obs = state.latest_observation
            if hasattr(obs, 'content') and 'error' in obs.content.lower():
                # Add error analysis to the context
                self._add_error_analysis_context(obs)
    
    def _enhance_action_quality(self, action: Action, state) -> Action:
        """Enhance action with quality improvements"""
        if hasattr(action, 'content'):
            # Add quality enhancements to code actions
            if 'def ' in action.content or 'class ' in action.content:
                action.content = self._add_quality_annotations(action.content)
        
        return action
    
    def _add_error_analysis_context(self, observation: Observation) -> None:
        """Add error analysis context for better debugging"""
        error_context = """
        Error Analysis Mode Activated:
        - Analyze the error message carefully
        - Identify the root cause, not just symptoms
        - Consider multiple potential solutions
        - Implement robust error handling
        - Add logging for future debugging
        """
        # This would be added to the agent's context in a real implementation
    
    def _add_quality_annotations(self, code: str) -> str:
        """Add quality annotations to generated code"""
        lines = code.split('\n')
        enhanced_lines = []
        
        for line in lines:
            enhanced_lines.append(line)
            
            # Add type hints reminder for function definitions
            if line.strip().startswith('def ') and '->' not in line:
                enhanced_lines.append('    # TODO: Add type hints for better code quality')
            
            # Add docstring reminder for classes
            if line.strip().startswith('class '):
                enhanced_lines.append('    """TODO: Add comprehensive class docstring"""')
        
        return '\n'.join(enhanced_lines)


class SecurityFocusedAgent(CodeActAgent):
    """
    Security-focused agent for handling sensitive operations
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.security_mode = True
    
    def get_system_message(self) -> str:
        return """You are a security-focused software engineer with expertise in:

🔒 SECURITY PRIORITIES:
- Input validation and sanitization
- Authentication and authorization
- Secure data handling and storage
- Protection against common vulnerabilities (OWASP Top 10)
- Secure coding practices
- Privacy and data protection compliance

🛡️ SECURITY PRACTICES:
- Always validate and sanitize user inputs
- Use parameterized queries for database operations
- Implement proper authentication mechanisms
- Handle sensitive data (passwords, tokens) securely
- Follow principle of least privilege
- Implement proper error handling without information leakage

🔍 SECURITY CHECKS:
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure session management
- Proper encryption and hashing
- Secure API design

Never compromise on security. When in doubt, choose the more secure approach."""


class PerformanceOptimizedAgent(CodeActAgent):
    """
    Performance-optimized agent for high-performance applications
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.performance_mode = True
    
    def get_system_message(self) -> str:
        return """You are a performance optimization expert with focus on:

⚡ PERFORMANCE PRIORITIES:
- Algorithm efficiency and complexity analysis
- Memory usage optimization
- Database query optimization
- Caching strategies
- Concurrent and parallel processing
- Resource management

🚀 OPTIMIZATION TECHNIQUES:
- Choose appropriate data structures
- Minimize computational complexity
- Implement efficient algorithms
- Use caching where beneficial
- Optimize database queries
- Consider memory allocation patterns

📊 PERFORMANCE MONITORING:
- Add performance metrics and logging
- Implement benchmarking
- Profile critical code paths
- Monitor resource usage
- Set up performance alerts

Always consider performance implications and optimize for scalability."""


class TestingSpecialistAgent(CodeActAgent):
    """
    Testing specialist agent focused on comprehensive testing
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.testing_mode = True
    
    def get_system_message(self) -> str:
        return """You are a testing specialist with expertise in:

🧪 TESTING STRATEGIES:
- Unit testing with high coverage
- Integration testing
- End-to-end testing
- Performance testing
- Security testing
- Accessibility testing

✅ TESTING BEST PRACTICES:
- Write tests before or alongside code (TDD/BDD)
- Test normal, edge, and error cases
- Use descriptive test names
- Maintain test independence
- Mock external dependencies appropriately
- Ensure tests are fast and reliable

🔧 TESTING TOOLS:
- pytest for Python
- Jest for JavaScript
- JUnit for Java
- Appropriate mocking frameworks
- Test coverage tools
- Continuous integration setup

Always write comprehensive tests that give confidence in code quality."""


class DocumentationExpertAgent(CodeActAgent):
    """
    Documentation expert agent for creating comprehensive documentation
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.documentation_mode = True
    
    def get_system_message(self) -> str:
        return """You are a documentation expert specializing in:

📚 DOCUMENTATION TYPES:
- API documentation
- User guides and tutorials
- Technical specifications
- Code comments and docstrings
- README files
- Architecture documentation

✍️ DOCUMENTATION STANDARDS:
- Clear and concise writing
- Comprehensive examples
- Step-by-step instructions
- Visual aids when helpful
- Up-to-date information
- Searchable and organized content

🎯 DOCUMENTATION GOALS:
- Make code self-documenting
- Provide clear usage examples
- Explain complex concepts simply
- Include troubleshooting guides
- Document edge cases and limitations
- Maintain consistency across all docs

Always prioritize clarity and completeness in documentation."""


# Agent factory for creating specialized agents
class QualityAgentFactory:
    """Factory for creating specialized quality agents"""
    
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig) -> CodeActAgent:
        """Create a specialized agent based on type"""
        agents = {
            'premium': PremiumCodeActAgent,
            'security': SecurityFocusedAgent,
            'performance': PerformanceOptimizedAgent,
            'testing': TestingSpecialistAgent,
            'documentation': DocumentationExpertAgent,
        }
        
        agent_class = agents.get(agent_type, PremiumCodeActAgent)
        return agent_class(config)
    
    @staticmethod
    def get_available_agents() -> List[str]:
        """Get list of available specialized agents"""
        return ['premium', 'security', 'performance', 'testing', 'documentation']


# Configuration helper
def get_quality_agent_config(agent_type: str = 'premium') -> Dict[str, Any]:
    """Get configuration for quality agents"""
    base_config = {
        'enable_browsing': True,
        'enable_llm_editor': True,
        'enable_editor': True,
        'enable_jupyter': True,
        'enable_cmd': True,
        'enable_think': True,
        'enable_finish': True,
        'enable_history_truncation': True,
        'enable_condensation_request': True,
        'enable_prompt_extensions': True,
    }
    
    # Agent-specific configurations
    agent_configs = {
        'premium': {
            **base_config,
            'llm_config': 'claude-sonnet',
            'max_iterations': 2000,
        },
        'security': {
            **base_config,
            'llm_config': 'gpt4o',
            'enable_security_analyzer': True,
            'confirmation_mode': True,
        },
        'performance': {
            **base_config,
            'llm_config': 'gpt4o',
            'enable_auto_lint': True,
        },
        'testing': {
            **base_config,
            'llm_config': 'gpt4o-mini',
            'enable_jupyter': True,
        },
        'documentation': {
            **base_config,
            'llm_config': 'gpt4o-mini',
            'enable_llm_editor': True,
        },
    }
    
    return agent_configs.get(agent_type, agent_configs['premium'])