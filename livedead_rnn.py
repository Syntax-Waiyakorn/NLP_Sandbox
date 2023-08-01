import torch
import torch.nn as nn
# import matplotlib.pyplot as plt
from utils import load_data, line_to_tensor, random_training_example

if torch.cuda.is_available():
    # Get the number of available GPUs
    num_gpus = torch.cuda.device_count()
    print(f"Number of available GPUs: {num_gpus}")

    # Choose the first GPU (you can choose any available GPU by changing the index)
    device = torch.device("cuda:0")

    # Set the default tensor type to CUDA tensors
    torch.set_default_tensor_type(torch.cuda.FloatTensor)

    print("CUDA is available and activated.")
else:
    # If CUDA is not available, use the CPU
    device = torch.device("cpu")
    print("CUDA is not available. Using CPU.")

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input_tensor, hidden_tensor):
        combined = torch.cat((input_tensor, hidden_tensor), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)

category_lines, all_categories = load_data()
n_categories = len(all_categories)
n_hidden = 128
rnn = RNN(87, n_hidden, n_categories)

def train(line_tensor, category_tensor):
    hidden = rnn.init_hidden()
    rnn.zero_grad()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    loss = criterion(output, category_tensor)

    loss.backward()
    optimizer.step()

    return output, loss.item()

criterion = nn.NLLLoss()
learning_rate = 0.005
optimizer = torch.optim.SGD(rnn.parameters(), lr=learning_rate)
current_loss = 0
all_losses = []
plot_steps, print_steps = 1000, 5000
n_iters = 100000

def category_from_output(output):
    category_idx = torch.argmax(output).item()
    return all_categories[category_idx]

for i in range(n_iters):
    category, line, category_tensor, line_tensor = random_training_example(category_lines, all_categories)
    
    output, loss = train(line_tensor, category_tensor)
    current_loss += loss

    if (i+1) % plot_steps == 0:
        all_losses.append(current_loss / plot_steps)
        current_loss = 0

    if (i+1) % print_steps == 0:
        guess = category_from_output(output)
        correct = "CORRECT" if guess == category else f"WRONG ({category})"
        print(f"{(i+1)/n_iters*100:.2f}% Loss: {loss:.4f} Word: {line} / Guess: {guess} --> {correct}")

# plt.figure()
# plt.plot(all_losses)
# plt.xlabel('Iterations')
# plt.ylabel('Loss')
# plt.title('Training Loss')
# plt.show()

print(all_losses)

def predict(input_line):
    print(f"\n> {input_line}")
    with torch.no_grad():
        line_tensor = line_to_tensor(input_line)
        hidden = rnn.init_hidden()

        for i in range(line_tensor.size()[0]):
            output, hidden = rnn(line_tensor[i], hidden)

        guess = category_from_output(output)
        print(guess)

while True:
    sentence = input("ใส่คำสะ (พิมพ์ 'ออก' เพื่อออก): ")
    if sentence.lower() == "ออก":
        break

    predict(sentence)