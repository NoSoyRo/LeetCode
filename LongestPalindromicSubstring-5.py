"""
5. Longest Palindromic Substring
Medium

Given a string s, return the longest palindromic substring in s.

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"

Constraints:
- 1 <= s.length <= 1000
- s consist of only digits and English letters.
"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Approach: Expand Around Centers
        
        For each character (and between characters), we expand around it
        to find the longest palindrome centered at that position.
        
        Time Complexity: O(n²)
        Space Complexity: O(1)
        """
        if not s:
            return ""
        
        start = 0
        max_len = 1
        
        def expand_around_center(left: int, right: int) -> int:
            """Helper function to expand around center and return length"""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1
        
        for i in range(len(s)):
            # Check for odd length palindromes (center is at i)
            len1 = expand_around_center(i, i)
            
            # Check for even length palindromes (center is between i and i+1)
            len2 = expand_around_center(i, i + 1)
            
            # Get the maximum length palindrome centered at i
            current_max = max(len1, len2)
            
            # Update the result if we found a longer palindrome
            if current_max > max_len:
                max_len = current_max
                start = i - (current_max - 1) // 2
        
        return s[start:start + max_len]
    
    def longestPalindrome_dp(self, s: str) -> str:
        """
        Alternative Approach: Dynamic Programming
        
        dp[i][j] represents whether substring s[i:j+1] is a palindrome
        
        Time Complexity: O(n²)
        Space Complexity: O(n²)
        """
        n = len(s)
        if n == 0:
            return ""
        
        # dp[i][j] will be True if substring s[i:j+1] is palindrome
        dp = [[False] * n for _ in range(n)]
        
        start = 0
        max_len = 1
        
        # Every single character is a palindrome
        for i in range(n):
            dp[i][i] = True
        
        # Check for palindromes of length 2
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                start = i
                max_len = 2
        
        # Check for palindromes of length 3 and more
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                # Check if s[i:j+1] is palindrome
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    start = i
                    max_len = length
        
        return s[start:start + max_len]
    
    def longestPalindrome_manacher(self, s: str) -> str:
        """
        Advanced Approach: Manacher's Algorithm
        
        Optimized algorithm for finding longest palindromes
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        # Transform string to handle even length palindromes
        # "abc" -> "#a#b#c#"
        transformed = '#'.join('^{}$'.format(s))
        n = len(transformed)
        
        # Array to store palindrome lengths
        P = [0] * n
        center = right = 0
        
        for i in range(1, n - 1):
            # Mirror of i with respect to center
            mirror = 2 * center - i
            
            if i < right:
                P[i] = min(right - i, P[mirror])
            
            # Try to expand palindrome centered at i
            try:
                while transformed[i + (1 + P[i])] == transformed[i - (1 + P[i])]:
                    P[i] += 1
            except IndexError:
                pass
            
            # If palindrome centered at i extends past right, adjust center and right
            if i + P[i] > right:
                center, right = i, i + P[i]
        
        # Find the longest palindrome
        max_len = max(P)
        center_index = P.index(max_len)
        
        # Extract the palindrome from original string
        start = (center_index - max_len) // 2
        return s[start:start + max_len]


def test_solution():
    """Test cases for the solution"""
    solution = Solution()
    
    test_cases = [
        "babad",      # Expected: "bab" or "aba"
        "cbbd",       # Expected: "bb"
        "a",          # Expected: "a"
        "ac",         # Expected: "a" or "c"
        "racecar",    # Expected: "racecar"
        "noon",       # Expected: "noon"
        "abcdef",     # Expected: any single character
        "aabbaa",     # Expected: "aabbaa"
        "",           # Expected: ""
    ]
    
    print("Testing Expand Around Centers approach:")
    for i, test in enumerate(test_cases):
        result = solution.longestPalindrome(test)
        print(f"Test {i+1}: '{test}' -> '{result}'")
    
    print("\nTesting Dynamic Programming approach:")
    for i, test in enumerate(test_cases):
        result = solution.longestPalindrome_dp(test)
        print(f"Test {i+1}: '{test}' -> '{result}'")
    
    print("\nTesting Manacher's Algorithm:")
    for i, test in enumerate(test_cases):
        result = solution.longestPalindrome_manacher(test)
        print(f"Test {i+1}: '{test}' -> '{result}'")


if __name__ == "__main__":
    test_solution()
