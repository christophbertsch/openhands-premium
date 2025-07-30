"""
Advanced Microagents for OpenHands
These microagents provide specialized capabilities for enhanced functionality
"""

import os
import json
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path


class CodeQualityMicroagent:
    """Microagent for code quality analysis and improvement"""
    
    def __init__(self):
        self.quality_rules = {
            'python': {
                'max_line_length': 88,
                'max_function_length': 50,
                'max_complexity': 10,
                'required_docstrings': True,
                'type_hints': True,
            },
            'javascript': {
                'max_line_length': 100,
                'max_function_length': 30,
                'prefer_const': True,
                'no_var': True,
                'semicolons': True,
            },
            'typescript': {
                'strict_mode': True,
                'no_any': True,
                'explicit_return_types': True,
            }
        }
    
    def analyze_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code quality and provide recommendations"""
        issues = []
        suggestions = []
        
        lines = code.split('\n')
        rules = self.quality_rules.get(language, {})
        
        # Check line length
        max_length = rules.get('max_line_length', 100)
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                issues.append(f"Line {i}: Exceeds maximum length ({len(line)} > {max_length})")
        
        # Language-specific checks
        if language == 'python':
            issues.extend(self._check_python_quality(code, lines))
        elif language in ['javascript', 'typescript']:
            issues.extend(self._check_js_quality(code, lines, language))
        
        # Generate suggestions
        if issues:
            suggestions = self._generate_quality_suggestions(issues, language)
        
        return {
            'quality_score': max(0, 100 - len(issues) * 5),
            'issues': issues,
            'suggestions': suggestions,
            'language': language
        }
    
    def _check_python_quality(self, code: str, lines: List[str]) -> List[str]:
        """Python-specific quality checks"""
        issues = []
        
        # Check for missing docstrings
        in_function = False
        function_line = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('def ') or stripped.startswith('class '):
                in_function = True
                function_line = i
            elif in_function and stripped.startswith('"""') or stripped.startswith("'''"):
                in_function = False
            elif in_function and stripped and not stripped.startswith('#'):
                if i - function_line > 1:
                    issues.append(f"Line {function_line + 1}: Missing docstring")
                    in_function = False
        
        # Check for type hints
        for i, line in enumerate(lines, 1):
            if 'def ' in line and '->' not in line and '__init__' not in line:
                issues.append(f"Line {i}: Missing return type hint")
        
        return issues
    
    def _check_js_quality(self, code: str, lines: List[str], language: str) -> List[str]:
        """JavaScript/TypeScript-specific quality checks"""
        issues = []
        
        # Check for var usage
        for i, line in enumerate(lines, 1):
            if 'var ' in line:
                issues.append(f"Line {i}: Use 'const' or 'let' instead of 'var'")
        
        # Check for missing semicolons
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if (stripped and not stripped.endswith((';', '{', '}', ':', ',')) 
                and not stripped.startswith(('if', 'for', 'while', 'function', 'class', '//'))):
                issues.append(f"Line {i}: Missing semicolon")
        
        return issues
    
    def _generate_quality_suggestions(self, issues: List[str], language: str) -> List[str]:
        """Generate improvement suggestions based on issues"""
        suggestions = []
        
        if any('docstring' in issue.lower() for issue in issues):
            suggestions.append("Add comprehensive docstrings to all functions and classes")
        
        if any('type hint' in issue.lower() for issue in issues):
            suggestions.append("Add type hints to improve code clarity and IDE support")
        
        if any('length' in issue.lower() for issue in issues):
            suggestions.append("Break long lines into multiple lines for better readability")
        
        if language == 'python':
            suggestions.append("Consider using tools like black, flake8, and mypy for automated quality checks")
        elif language in ['javascript', 'typescript']:
            suggestions.append("Consider using ESLint and Prettier for automated code formatting")
        
        return suggestions


class SecurityMicroagent:
    """Microagent for security analysis and recommendations"""
    
    def __init__(self):
        self.security_patterns = {
            'sql_injection': [
                r'execute\s*\(\s*["\'].*%.*["\']',
                r'query\s*\(\s*["\'].*\+.*["\']',
                r'SELECT.*\+.*FROM',
            ],
            'xss_vulnerability': [
                r'innerHTML\s*=.*\+',
                r'document\.write\s*\(',
                r'eval\s*\(',
            ],
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
            ],
            'insecure_random': [
                r'Math\.random\(\)',
                r'random\.random\(\)',
            ]
        }
    
    def analyze_security(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code for security vulnerabilities"""
        import re
        
        vulnerabilities = []
        recommendations = []
        
        for vuln_type, patterns in self.security_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        'type': vuln_type,
                        'line': line_num,
                        'pattern': match.group(),
                        'severity': self._get_severity(vuln_type)
                    })
        
        # Generate recommendations
        recommendations = self._generate_security_recommendations(vulnerabilities, language)
        
        return {
            'security_score': max(0, 100 - len(vulnerabilities) * 10),
            'vulnerabilities': vulnerabilities,
            'recommendations': recommendations,
            'language': language
        }
    
    def _get_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type"""
        severity_map = {
            'sql_injection': 'HIGH',
            'xss_vulnerability': 'HIGH',
            'hardcoded_secrets': 'MEDIUM',
            'insecure_random': 'LOW'
        }
        return severity_map.get(vuln_type, 'MEDIUM')
    
    def _generate_security_recommendations(self, vulnerabilities: List[Dict], language: str) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        vuln_types = {v['type'] for v in vulnerabilities}
        
        if 'sql_injection' in vuln_types:
            recommendations.append("Use parameterized queries or ORM to prevent SQL injection")
        
        if 'xss_vulnerability' in vuln_types:
            recommendations.append("Sanitize user input and use safe DOM manipulation methods")
        
        if 'hardcoded_secrets' in vuln_types:
            recommendations.append("Use environment variables or secure vaults for secrets")
        
        if 'insecure_random' in vuln_types:
            recommendations.append("Use cryptographically secure random number generators")
        
        # General recommendations
        recommendations.extend([
            "Implement input validation for all user inputs",
            "Use HTTPS for all communications",
            "Implement proper authentication and authorization",
            "Keep dependencies up to date",
            "Follow OWASP security guidelines"
        ])
        
        return recommendations


class PerformanceMicroagent:
    """Microagent for performance analysis and optimization"""
    
    def __init__(self):
        self.performance_patterns = {
            'inefficient_loops': [
                r'for.*in.*range\(len\(',
                r'while.*len\(',
            ],
            'string_concatenation': [
                r'\+\s*["\'].*["\']',
                r'["\'].*["\'].*\+',
            ],
            'repeated_calculations': [
                r'for.*:.*\n.*for.*:.*\n.*\1',
            ],
            'memory_leaks': [
                r'global\s+\w+\s*=\s*\[\]',
                r'cache\s*=\s*\{\}',
            ]
        }
    
    def analyze_performance(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code for performance issues"""
        import re
        
        issues = []
        optimizations = []
        
        for issue_type, patterns in self.performance_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    issues.append({
                        'type': issue_type,
                        'line': line_num,
                        'pattern': match.group(),
                        'impact': self._get_performance_impact(issue_type)
                    })
        
        # Generate optimization suggestions
        optimizations = self._generate_performance_optimizations(issues, language)
        
        return {
            'performance_score': max(0, 100 - len(issues) * 8),
            'issues': issues,
            'optimizations': optimizations,
            'language': language
        }
    
    def _get_performance_impact(self, issue_type: str) -> str:
        """Get performance impact level"""
        impact_map = {
            'inefficient_loops': 'HIGH',
            'string_concatenation': 'MEDIUM',
            'repeated_calculations': 'HIGH',
            'memory_leaks': 'HIGH'
        }
        return impact_map.get(issue_type, 'MEDIUM')
    
    def _generate_performance_optimizations(self, issues: List[Dict], language: str) -> List[str]:
        """Generate performance optimization suggestions"""
        optimizations = []
        
        issue_types = {i['type'] for i in issues}
        
        if 'inefficient_loops' in issue_types:
            optimizations.append("Use enumerate() instead of range(len()) for better performance")
        
        if 'string_concatenation' in issue_types:
            if language == 'python':
                optimizations.append("Use f-strings or join() for string concatenation")
            else:
                optimizations.append("Use template literals or array join for string building")
        
        if 'repeated_calculations' in issue_types:
            optimizations.append("Cache repeated calculations outside loops")
        
        if 'memory_leaks' in issue_types:
            optimizations.append("Avoid global mutable state and implement proper cleanup")
        
        # General optimizations
        optimizations.extend([
            "Use appropriate data structures for your use case",
            "Consider algorithmic complexity (Big O notation)",
            "Profile your code to identify bottlenecks",
            "Use lazy evaluation where possible",
            "Implement caching for expensive operations"
        ])
        
        return optimizations


class TestingMicroagent:
    """Microagent for testing analysis and test generation"""
    
    def __init__(self):
        self.test_patterns = {
            'python': {
                'test_files': [r'test_.*\.py$', r'.*_test\.py$'],
                'test_functions': [r'def test_.*\('],
                'assertions': [r'assert\s+', r'self\.assert'],
            },
            'javascript': {
                'test_files': [r'.*\.test\.js$', r'.*\.spec\.js$'],
                'test_functions': [r'it\s*\(', r'test\s*\('],
                'assertions': [r'expect\s*\(', r'assert\.'],
            }
        }
    
    def analyze_test_coverage(self, project_path: str, language: str) -> Dict[str, Any]:
        """Analyze test coverage and quality"""
        import glob
        import re
        
        project_files = []
        test_files = []
        
        # Find all source files
        if language == 'python':
            project_files = glob.glob(f"{project_path}/**/*.py", recursive=True)
            project_files = [f for f in project_files if not f.endswith('_test.py') and not f.startswith('test_')]
        elif language == 'javascript':
            project_files = glob.glob(f"{project_path}/**/*.js", recursive=True)
            project_files = [f for f in project_files if not f.endswith('.test.js') and not f.endswith('.spec.js')]
        
        # Find test files
        patterns = self.test_patterns.get(language, {}).get('test_files', [])
        for pattern in patterns:
            test_files.extend(glob.glob(f"{project_path}/**/{pattern}", recursive=True))
        
        # Calculate coverage metrics
        total_files = len(project_files)
        tested_files = len(test_files)
        coverage_ratio = tested_files / total_files if total_files > 0 else 0
        
        # Analyze test quality
        test_quality = self._analyze_test_quality(test_files, language)
        
        return {
            'coverage_ratio': coverage_ratio,
            'total_files': total_files,
            'test_files': tested_files,
            'test_quality': test_quality,
            'recommendations': self._generate_testing_recommendations(coverage_ratio, test_quality)
        }
    
    def _analyze_test_quality(self, test_files: List[str], language: str) -> Dict[str, Any]:
        """Analyze quality of existing tests"""
        import re
        
        total_tests = 0
        total_assertions = 0
        
        patterns = self.test_patterns.get(language, {})
        
        for test_file in test_files:
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                
                # Count test functions
                for pattern in patterns.get('test_functions', []):
                    total_tests += len(re.findall(pattern, content))
                
                # Count assertions
                for pattern in patterns.get('assertions', []):
                    total_assertions += len(re.findall(pattern, content))
            
            except Exception:
                continue
        
        assertions_per_test = total_assertions / total_tests if total_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'total_assertions': total_assertions,
            'assertions_per_test': assertions_per_test,
            'quality_score': min(100, assertions_per_test * 20)
        }
    
    def _generate_testing_recommendations(self, coverage_ratio: float, test_quality: Dict[str, Any]) -> List[str]:
        """Generate testing recommendations"""
        recommendations = []
        
        if coverage_ratio < 0.8:
            recommendations.append(f"Increase test coverage (currently {coverage_ratio:.1%})")
        
        if test_quality['assertions_per_test'] < 2:
            recommendations.append("Add more assertions per test for better validation")
        
        recommendations.extend([
            "Write tests for edge cases and error conditions",
            "Use descriptive test names that explain what's being tested",
            "Implement integration tests for complex workflows",
            "Add performance tests for critical operations",
            "Use mocking for external dependencies",
            "Set up continuous integration for automated testing"
        ])
        
        return recommendations


class DocumentationMicroagent:
    """Microagent for documentation analysis and generation"""
    
    def __init__(self):
        self.doc_patterns = {
            'python': {
                'docstrings': [r'""".*?"""', r"'''.*?'''"],
                'comments': [r'#.*'],
                'type_hints': [r':\s*\w+', r'->\s*\w+'],
            },
            'javascript': {
                'jsdoc': [r'/\*\*.*?\*/', r'@param', r'@returns'],
                'comments': [r'//.*', r'/\*.*?\*/'],
            }
        }
    
    def analyze_documentation(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze documentation quality"""
        import re
        
        lines = code.split('\n')
        total_lines = len([l for l in lines if l.strip()])
        
        # Count documentation elements
        docstring_count = 0
        comment_count = 0
        
        patterns = self.doc_patterns.get(language, {})
        
        # Count docstrings/JSDoc
        for pattern in patterns.get('docstrings', []) + patterns.get('jsdoc', []):
            docstring_count += len(re.findall(pattern, code, re.DOTALL))
        
        # Count comments
        for pattern in patterns.get('comments', []):
            comment_count += len(re.findall(pattern, code))
        
        # Calculate documentation ratio
        doc_ratio = (docstring_count + comment_count) / total_lines if total_lines > 0 else 0
        
        # Analyze function documentation
        function_doc_analysis = self._analyze_function_documentation(code, language)
        
        return {
            'documentation_ratio': doc_ratio,
            'docstring_count': docstring_count,
            'comment_count': comment_count,
            'function_documentation': function_doc_analysis,
            'recommendations': self._generate_documentation_recommendations(doc_ratio, function_doc_analysis)
        }
    
    def _analyze_function_documentation(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze function-level documentation"""
        import re
        
        if language == 'python':
            functions = re.findall(r'def\s+(\w+)\s*\([^)]*\):', code)
            documented_functions = re.findall(r'def\s+\w+\s*\([^)]*\):\s*\n\s*"""', code)
        else:
            functions = re.findall(r'function\s+(\w+)\s*\(', code)
            documented_functions = re.findall(r'function\s+\w+\s*\([^)]*\)\s*{\s*/\*\*', code)
        
        total_functions = len(functions)
        documented_count = len(documented_functions)
        
        return {
            'total_functions': total_functions,
            'documented_functions': documented_count,
            'documentation_coverage': documented_count / total_functions if total_functions > 0 else 0
        }
    
    def _generate_documentation_recommendations(self, doc_ratio: float, function_analysis: Dict[str, Any]) -> List[str]:
        """Generate documentation recommendations"""
        recommendations = []
        
        if doc_ratio < 0.1:
            recommendations.append("Add more comments and documentation to improve code readability")
        
        if function_analysis['documentation_coverage'] < 0.8:
            recommendations.append("Add docstrings/JSDoc to all public functions")
        
        recommendations.extend([
            "Include parameter descriptions and return value documentation",
            "Add usage examples for complex functions",
            "Document any side effects or exceptions",
            "Keep documentation up to date with code changes",
            "Use consistent documentation style throughout the project",
            "Consider generating API documentation automatically"
        ])
        
        return recommendations


# Microagent orchestrator
class MicroagentOrchestrator:
    """Orchestrates multiple microagents for comprehensive analysis"""
    
    def __init__(self):
        self.microagents = {
            'quality': CodeQualityMicroagent(),
            'security': SecurityMicroagent(),
            'performance': PerformanceMicroagent(),
            'testing': TestingMicroagent(),
            'documentation': DocumentationMicroagent(),
        }
    
    def comprehensive_analysis(self, code: str, language: str, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Run comprehensive analysis using all microagents"""
        results = {}
        
        # Run code-based analyses
        results['quality'] = self.microagents['quality'].analyze_code_quality(code, language)
        results['security'] = self.microagents['security'].analyze_security(code, language)
        results['performance'] = self.microagents['performance'].analyze_performance(code, language)
        results['documentation'] = self.microagents['documentation'].analyze_documentation(code, language)
        
        # Run project-based analyses if project path is provided
        if project_path:
            results['testing'] = self.microagents['testing'].analyze_test_coverage(project_path, language)
        
        # Calculate overall score
        scores = [r.get('quality_score', 0) or r.get('security_score', 0) or r.get('performance_score', 0) 
                 for r in results.values() if isinstance(r, dict)]
        overall_score = sum(scores) / len(scores) if scores else 0
        
        results['overall_score'] = overall_score
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis summary"""
        total_issues = 0
        total_recommendations = 0
        
        for analysis in results.values():
            if isinstance(analysis, dict):
                total_issues += len(analysis.get('issues', []))
                total_issues += len(analysis.get('vulnerabilities', []))
                total_recommendations += len(analysis.get('recommendations', []))
                total_recommendations += len(analysis.get('suggestions', []))
                total_recommendations += len(analysis.get('optimizations', []))
        
        return {
            'total_issues': total_issues,
            'total_recommendations': total_recommendations,
            'analysis_types': list(results.keys()),
            'overall_health': 'Good' if results.get('overall_score', 0) > 80 else 'Needs Improvement'
        }