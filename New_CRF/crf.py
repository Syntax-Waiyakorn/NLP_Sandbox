import torch
import torch.nn as nn
import torch.optim as optim
from data.crf_segmentation import X_train, Y_train, labels
from torchcrf import CRF
from utils import DataLoader, embed


print(X_train)
embedded = DataLoader()
tag_to_idx = {}
for sent_tags in Y_train:
    for tag in sent_tags:
        if tag not in tag_to_idx:
            tag_to_idx[tag] = len(tag_to_idx)

Y_train_idx = [[tag_to_idx[tag] for tag in word_tags] for word_tags in Y_train]

class CRFModel(nn.Module):
    def __init__(self, num_tags):
        super(CRFModel, self).__init__()
        self.linear = nn.Linear(68, num_tags)
        self.crf = CRF(num_tags, batch_first=True)
    
    def forward(self, x):
        emissions = self.linear(x)
        return emissions

num_tags = len(tag_to_idx)
model = CRFModel(num_tags)

criterion = model.crf
optimizer = optim.SGD(model.parameters(), lr = 0.001)

num_epochs = 1
for epoch in range(num_epochs):
    model.train()   
    total_loss = 0
    
    for inputs, targets, label in zip(X_train, Y_train_idx, labels):
        bruh = embed("ipa", inputs, embedded).unsqueeze(0)
        targets = torch.tensor(targets).unsqueeze(0)
        print(label)
        optimizer.zero_grad()
        outputs = model(bruh)
        print(outputs.shape)
        loss = -criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / len(X_train)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

while True:
    input_sentence = input("Enter a sentence: ").split()
    input_word = [(char)for char in input_sentence[0]]
    input_tensor = embed("one_hot", input_word, embedded).unsqueeze(0)

    model.eval()

    with torch.no_grad():
        emissions = model(input_tensor)

    with torch.no_grad():
        predicted_tags = model.crf.decode(emissions)

    print(predicted_tags)
    predicted_tags = [list(tag_to_idx.keys())[idx] for idx in predicted_tags[0]]
    print("Predicted Tags:", " ".join(predicted_tags))