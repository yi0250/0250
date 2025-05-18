# Leetcode-Rust-66-Plus One

```rust
impl Solution {
    pub fn plus_one(digits: Vec<i32>) -> Vec<i32> {
        // 將輸入轉為可變的 Vec
        let mut digits = digits;
        // 從最低有效位开始處理進位
        for i in (0..digits.len()).rev() {
            if digits[i] < 9 {
                digits[i] += 1;
                return digits;
            }
            digits[i] = 0;
        }
        // 全部為 9 時需要在最前面加一位
        let mut result = Vec::with_capacity(digits.len() + 1);
        result.push(1);
        result.extend(digits);
        result
    }
}
```

## Case1
### Input

```rust
[1,2,3]
```

### Output

```rust
[1,2,4]
```

## Case2
### Input

```rust
[4,3,2,1]
```

### Output

```rust
[4,3,2,2]
```

## Case3
### Input

```rust
[9]
```

### Output

```rust
[1,0]
```

# Leetcode-Rust-01-Two Sum

```rust
impl Solution {
    pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
        use std::collections::HashMap;
        let mut map = HashMap::with_capacity(nums.len());
        for (i, &num) in nums.iter().enumerate() {
            let complement = target - num;
            if let Some(&j) = map.get(&complement) {
                return vec![j as i32, i as i32];
            }
            map.insert(num, i);
        }
        // 按題意保證有解，不會執行到這
        vec![]
    }
}
```

## Case1
### Input

```rust
nums=[2,7,11,15]
target=9
```

### Output

```rust
[0,1]
```

## Case2
### Input

```rust
nums=[3,2,4]
target=6
```

### Output

```rust
[1,2]
```

## Case3
### Input

```rust
nums=[3,3]
target=6
```

### Output

```rust
[0,1]
```
