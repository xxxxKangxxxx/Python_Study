# def mini_mnist():
#     """
#     8x8 숫자 이미지 분류 (sklearn digits 데이터셋 사용)
#     """
#     from sklearn.datasets import load_digits
#     from sklearn.model_selection import train_test_split
#     import numpy as np
#     import matplotlib.pyplot as plt
    
#     # 데이터 로드
#     digits = load_digits()
#     X, y = digits.data, digits.target
#     X = X / 16.0  # 정규화 (0-16 → 0-1)
    
#     # 원-핫 인코딩
#     y_onehot = np.eye(10)[y]
    
#     # 훈련/테스트 분할
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y_onehot, test_size=0.2, random_state=42
#     )
    
#     print("미니 MNIST 과제")
#     print(f"훈련 데이터: {X_train.shape}")
#     print(f"테스트 데이터: {X_test.shape}")
#     print(f"클래스 수: 10개 (0-9 숫자)")
    
#     # TODO: 다층 클래스 분류 신경망 구현
#     # 1. 입력층: 64개 (8x8 이미지)
#     # 2. 은닉층: 적절한 크기
#     # 3. 출력층: 10개 (0-9 숫자)
#     # 4. Softmax 활성화 함수
#     # 5. Cross-Entropy 손실 함수
    
#     class DigitClassifier:
#         def __init__(self):
#             # 네트워크 구조 설계
#             self.input_size = 64    # 8x8 = 64 픽셀
#             self.hidden_size = 512  # 은닉층 뉴런 수
#             self.output_size = 10   # 0-9 숫자 클래스
            
#             # 가중치 초기화 (Xavier 초기화)
#             self.W1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2.0 / self.input_size)
#             self.b1 = np.zeros((1, self.hidden_size))
#             self.W2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2.0 / self.hidden_size)
#             self.b2 = np.zeros((1, self.output_size))
            
#             # 학습률
#             self.learning_rate = 0.01
        
#         def relu(self, z):
#             """ReLU 활성화 함수"""
#             return np.maximum(0, z)
        
#         def relu_derivative(self, z):
#             """ReLU 도함수"""
#             return (z > 0).astype(float)
        
#         def softmax(self, z):
#             """Softmax 활성화 함수"""
#             exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # 수치 안정성
#             return exp_z / np.sum(exp_z, axis=1, keepdims=True)
        
#         def cross_entropy_loss(self, y_pred, y_true):
#             """Cross-Entropy 손실 구현"""
#             # 수치 안정성을 위해 작은 값 추가
#             epsilon = 1e-15
#             y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
            
#             m = y_true.shape[0]
#             loss = -np.sum(y_true * np.log(y_pred)) / m
#             return loss
        
#         def forward(self, X):
#             """순전파"""
#             # 입력층 → 은닉층
#             self.z1 = np.dot(X, self.W1) + self.b1
#             self.a1 = self.relu(self.z1)
            
#             # 은닉층 → 출력층
#             self.z2 = np.dot(self.a1, self.W2) + self.b2
#             self.a2 = self.softmax(self.z2)
            
#             return self.a2
        
#         def backward(self, X, y):
#             """역전파"""
#             m = X.shape[0]
            
#             # 출력층 오차
#             dz2 = self.a2 - y
#             dW2 = np.dot(self.a1.T, dz2) / m
#             db2 = np.sum(dz2, axis=0, keepdims=True) / m
            
#             # 은닉층 오차
#             da1 = np.dot(dz2, self.W2.T)
#             dz1 = da1 * self.relu_derivative(self.z1)
#             dW1 = np.dot(X.T, dz1) / m
#             db1 = np.sum(dz1, axis=0, keepdims=True) / m
            
#             # 가중치 업데이트
#             self.W2 -= self.learning_rate * dW2
#             self.b2 -= self.learning_rate * db2
#             self.W1 -= self.learning_rate * dW1
#             self.b1 -= self.learning_rate * db1
        
#         def predict(self, X):
#             """예측 함수"""
#             output = self.forward(X)
#             return np.argmax(output, axis=1)
        
#         def accuracy(self, X, y):
#             """정확도 계산"""
#             predictions = self.predict(X)
#             true_labels = np.argmax(y, axis=1)
#             return np.mean(predictions == true_labels)
    
#     # 모델 생성 및 훈련
#     model = DigitClassifier()
    
#     # 훈련 과정
#     epochs = 1000
#     train_losses = []
#     train_accuracies = []
#     test_accuracies = []
    
#     print("\n훈련 시작...")
#     for epoch in range(epochs):
#         # 순전파
#         y_pred = model.forward(X_train)
        
#         # 손실 계산
#         loss = model.cross_entropy_loss(y_pred, y_train)
#         train_losses.append(loss)
        
#         # 역전파
#         model.backward(X_train, y_train)
        
#         # 정확도 계산 (매 100 에포크마다)
#         if epoch % 100 == 0:
#             train_acc = model.accuracy(X_train, y_train)
#             test_acc = model.accuracy(X_test, y_test)
#             train_accuracies.append(train_acc)
#             test_accuracies.append(test_acc)
            
#             print(f"Epoch {epoch:4d} | Loss: {loss:.4f} | Train Acc: {train_acc:.3f} | Test Acc: {test_acc:.3f}")
    
#     # 최종 결과
#     final_train_acc = model.accuracy(X_train, y_train)
#     final_test_acc = model.accuracy(X_test, y_test)
    
#     print("\n=== 최종 결과 ===")
#     print(f"훈련 정확도: {final_train_acc:.1%}")
#     print(f"테스트 정확도: {final_test_acc:.1%}")
    
#     # 목표 달성 확인
#     print("\n구현 후 다음을 확인하세요:")
#     if final_train_acc >= 0.90:
#         print("✓ 훈련 정확도: 90% 이상 달성!")
#     else:
#         print("✗ 훈련 정확도: 90% 이상 필요")
    
#     if final_test_acc >= 0.85:
#         print("✓ 테스트 정확도: 85% 이상 달성!")
#     else:
#         print("✗ 테스트 정확도: 85% 이상 필요")
    
#     print("- 각 숫자별 예측 성능 분석")
    
#     # 학습 곡선 시각화
#     plt.figure(figsize=(15, 5))
    
#     # 손실 곡선
#     plt.subplot(1, 3, 1)
#     plt.plot(train_losses)
#     plt.title('Training Loss')
#     plt.xlabel('Epoch')
#     plt.ylabel('Cross-Entropy Loss')
#     plt.grid(True)
    
#     # 정확도 곡선
#     plt.subplot(1, 3, 2)
#     epochs_acc = np.arange(0, epochs, 100)
#     plt.plot(epochs_acc, train_accuracies, label='Train')
#     plt.plot(epochs_acc, test_accuracies, label='Test')
#     plt.title('Accuracy')
#     plt.xlabel('Epoch')
#     plt.ylabel('Accuracy')
#     plt.legend()
#     plt.grid(True)
    
#     # 샘플 예측 결과
#     plt.subplot(1, 3, 3)
#     sample_idx = np.random.choice(len(X_test), 16)
#     sample_images = X_test[sample_idx].reshape(-1, 8, 8)
#     sample_predictions = model.predict(X_test[sample_idx])
#     sample_true = np.argmax(y_test[sample_idx], axis=1)
    
#     for i in range(16):
#         plt.subplot(4, 4, i+1)
#         plt.imshow(sample_images[i], cmap='gray')
#         color = 'green' if sample_predictions[i] == sample_true[i] else 'red'
#         plt.title(f'P:{sample_predictions[i]} T:{sample_true[i]}', color=color, fontsize=8)
#         plt.axis('off')
    
#     plt.tight_layout()
#     plt.show()
    
#     return model, final_train_acc, final_test_acc

# # 실행
# if __name__ == "__main__":
#     mini_mnist()

def mini_mnist():
    """
    8x8 숫자 이미지 분류 (sklearn digits 데이터셋 사용)
    """
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    import numpy as np
    import matplotlib.pyplot as plt
    
    # 데이터 로드
    digits = load_digits()
    X, y = digits.data, digits.target
    X = X / 16.0  # 정규화 (0-16 → 0-1)
    
    # 원-핫 인코딩
    y_onehot = np.eye(10)[y]
    
    # 훈련/테스트 분할
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_onehot, test_size=0.2, random_state=42
    )
    
    print("미니 MNIST 과제")
    print(f"훈련 데이터: {X_train.shape}")
    print(f"테스트 데이터: {X_test.shape}")
    print(f"클래스 수: 10개 (0-9 숫자)")
    
    # TODO: 다층 클래스 분류 신경망 구현
    # 1. 입력층: 64개 (8x8 이미지)
    # 2. 은닉층: 적절한 크기
    # 3. 출력층: 10개 (0-9 숫자)
    # 4. Softmax 활성화 함수
    # 5. Cross-Entropy 손실 함수
    
    class DigitClassifier:
        def __init__(self):
            # 네트워크 구조 설계
            self.input_size = 64    # 8x8 = 64 픽셀
            self.hidden_size = 512  # 은닉층 뉴런 수
            self.output_size = 10   # 0-9 숫자 클래스
            
            # 가중치 초기화 (Xavier 초기화)
            self.W1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2.0 / self.input_size)
            self.b1 = np.zeros((1, self.hidden_size))
            self.W2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2.0 / self.hidden_size)
            self.b2 = np.zeros((1, self.output_size))
            
            # Adam 옵티마이저 하이퍼파라미터
            self.learning_rate = 0.001  # Adam에서는 더 작은 학습률 사용
            self.beta1 = 0.9           # 1차 모멘트 감쇠율
            self.beta2 = 0.999         # 2차 모멘트 감쇠율
            self.epsilon = 1e-8        # 수치 안정성을 위한 작은 값
            
            # Adam 옵티마이저를 위한 모멘트 변수들
            self.m_W1 = np.zeros_like(self.W1)  # 1차 모멘트 (평균)
            self.v_W1 = np.zeros_like(self.W1)  # 2차 모멘트 (분산)
            self.m_b1 = np.zeros_like(self.b1)
            self.v_b1 = np.zeros_like(self.b1)
            self.m_W2 = np.zeros_like(self.W2)
            self.v_W2 = np.zeros_like(self.W2)
            self.m_b2 = np.zeros_like(self.b2)
            self.v_b2 = np.zeros_like(self.b2)
            
            self.t = 0  # 시간 스텝
        
        def relu(self, z):
            """ReLU 활성화 함수"""
            return np.maximum(0, z)
        
        def relu_derivative(self, z):
            """ReLU 도함수"""
            return (z > 0).astype(float)
        
        def softmax(self, z):
            """Softmax 활성화 함수"""
            exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # 수치 안정성
            return exp_z / np.sum(exp_z, axis=1, keepdims=True)
        
        def cross_entropy_loss(self, y_pred, y_true):
            """Cross-Entropy 손실 구현"""
            # 수치 안정성을 위해 작은 값 추가
            epsilon = 1e-15
            y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
            
            m = y_true.shape[0]
            loss = -np.sum(y_true * np.log(y_pred)) / m
            return loss
        
        def forward(self, X):
            """순전파"""
            # 입력층 → 은닉층
            self.z1 = np.dot(X, self.W1) + self.b1
            self.a1 = self.relu(self.z1)
            
            # 은닉층 → 출력층
            self.z2 = np.dot(self.a1, self.W2) + self.b2
            self.a2 = self.softmax(self.z2)
            
            return self.a2
        
        def adam_update(self, param, grad, m, v):
            """Adam 옵티마이저 업데이트"""
            self.t += 1  # 시간 스텝 증가
            
            # 1차 모멘트 (평균) 업데이트
            m = self.beta1 * m + (1 - self.beta1) * grad
            
            # 2차 모멘트 (분산) 업데이트  
            v = self.beta2 * v + (1 - self.beta2) * (grad ** 2)
            
            # 편향 보정 (bias correction)
            m_corrected = m / (1 - self.beta1 ** self.t)
            v_corrected = v / (1 - self.beta2 ** self.t)
            
            # 파라미터 업데이트
            param -= self.learning_rate * m_corrected / (np.sqrt(v_corrected) + self.epsilon)
            
            return param, m, v
        
        def backward(self, X, y):
            """역전파 (Adam 옵티마이저 사용)"""
            m = X.shape[0]
            
            # 출력층 오차
            dz2 = self.a2 - y
            dW2 = np.dot(self.a1.T, dz2) / m
            db2 = np.sum(dz2, axis=0, keepdims=True) / m
            
            # 은닉층 오차
            da1 = np.dot(dz2, self.W2.T)
            dz1 = da1 * self.relu_derivative(self.z1)
            dW1 = np.dot(X.T, dz1) / m
            db1 = np.sum(dz1, axis=0, keepdims=True) / m
            
            # Adam 옵티마이저로 가중치 업데이트
            self.W2, self.m_W2, self.v_W2 = self.adam_update(self.W2, dW2, self.m_W2, self.v_W2)
            self.b2, self.m_b2, self.v_b2 = self.adam_update(self.b2, db2, self.m_b2, self.v_b2)
            self.W1, self.m_W1, self.v_W1 = self.adam_update(self.W1, dW1, self.m_W1, self.v_W1)
            self.b1, self.m_b1, self.v_b1 = self.adam_update(self.b1, db1, self.m_b1, self.v_b1)
        
        def predict(self, X):
            """예측 함수"""
            output = self.forward(X)
            return np.argmax(output, axis=1)
        
        def accuracy(self, X, y):
            """정확도 계산"""
            predictions = self.predict(X)
            true_labels = np.argmax(y, axis=1)
            return np.mean(predictions == true_labels)
    
    # 모델 생성 및 훈련
    model = DigitClassifier()
    
    # 훈련 과정
    epochs = 1000
    train_losses = []
    train_accuracies = []
    test_accuracies = []
    
    print("\n훈련 시작... (Adam 옵티마이저 사용)")
    for epoch in range(epochs):
        # 순전파
        y_pred = model.forward(X_train)
        
        # 손실 계산
        loss = model.cross_entropy_loss(y_pred, y_train)
        train_losses.append(loss)
        
        # 역전파 (Adam 옵티마이저)
        model.backward(X_train, y_train)
        
        # 정확도 계산 (매 100 에포크마다)
        if epoch % 100 == 0:
            train_acc = model.accuracy(X_train, y_train)
            test_acc = model.accuracy(X_test, y_test)
            train_accuracies.append(train_acc)
            test_accuracies.append(test_acc)
            
            print(f"Epoch {epoch:4d} | Loss: {loss:.4f} | Train Acc: {train_acc:.3f} | Test Acc: {test_acc:.3f}")
    
    # 최종 결과
    final_train_acc = model.accuracy(X_train, y_train)
    final_test_acc = model.accuracy(X_test, y_test)
    
    print("\n=== 최종 결과 ===")
    print(f"훈련 정확도: {final_train_acc:.1%}")
    print(f"테스트 정확도: {final_test_acc:.1%}")
    
    # 목표 달성 확인
    print("\n구현 후 다음을 확인하세요:")
    if final_train_acc >= 0.90:
        print("✓ 훈련 정확도: 90% 이상 달성!")
    else:
        print("✗ 훈련 정확도: 90% 이상 필요")
    
    if final_test_acc >= 0.85:
        print("✓ 테스트 정확도: 85% 이상 달성!")
    else:
        print("✗ 테스트 정확도: 85% 이상 필요")
    
    print("- 각 숫자별 예측 성능 분석")
    
    # 학습 곡선 시각화
    plt.figure(figsize=(15, 5))
    
    # 손실 곡선
    plt.subplot(1, 3, 1)
    plt.plot(train_losses)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Cross-Entropy Loss')
    plt.grid(True)
    
    # 정확도 곡선
    plt.subplot(1, 3, 2)
    epochs_acc = np.arange(0, epochs, 100)
    plt.plot(epochs_acc, train_accuracies, label='Train')
    plt.plot(epochs_acc, test_accuracies, label='Test')
    plt.title('Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # 샘플 예측 결과
    plt.subplot(1, 3, 3)
    sample_idx = np.random.choice(len(X_test), 16)
    sample_images = X_test[sample_idx].reshape(-1, 8, 8)
    sample_predictions = model.predict(X_test[sample_idx])
    sample_true = np.argmax(y_test[sample_idx], axis=1)
    
    for i in range(16):
        plt.subplot(4, 4, i+1)
        plt.imshow(sample_images[i], cmap='gray')
        color = 'green' if sample_predictions[i] == sample_true[i] else 'red'
        plt.title(f'P:{sample_predictions[i]} T:{sample_true[i]}', color=color, fontsize=8)
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return model, final_train_acc, final_test_acc

# 실행
if __name__ == "__main__":
    mini_mnist()