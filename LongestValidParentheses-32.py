def longestValidParentheses(s: str) -> int:
    max_len = 0
    stack = [-1]  # piso
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)  # nuevo piso
            else:
                max_len = max(max_len, i - stack[-1])
    return max_len
