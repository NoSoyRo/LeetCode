class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        def findMedianHelper(A, B):
            m, n = len(A), len(B)
            if m > n:
                return findMedianHelper(B, A)  # Garantizar que A sea el más corto
            
            low, high = 0, m
            while low <= high:
                partitionA = (low + high) // 2
                partitionB = (m + n + 1) // 2 - partitionA
                
                maxLeftA = float('-inf') if partitionA == 0 else A[partitionA - 1]
                minRightA = float('inf') if partitionA == m else A[partitionA]
                
                maxLeftB = float('-inf') if partitionB == 0 else B[partitionB - 1]
                minRightB = float('inf') if partitionB == n else B[partitionB]
                
                if maxLeftA <= minRightB and maxLeftB <= minRightA:
                    if (m + n) % 2 == 0:
                        return (max(maxLeftA, maxLeftB) + min(minRightA, minRightB)) / 2.0
                    else:
                        return max(maxLeftA, maxLeftB)
                elif maxLeftA > minRightB:
                    high = partitionA - 1
                else:
                    low = partitionA + 1
            
            raise ValueError("Input arrays are not sorted correctly")
        
        return findMedianHelper(nums1, nums2)