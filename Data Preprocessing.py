# Normalize Data
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

start_date = datetime(2015, 12, 14)
end_date = datetime(2024, 12, 14)
ticker = 'TSLA'
data = yf.download(ticker, start = start_date, end = end_date, auto_adjust=False)
data['Date'] = data.index
price = data[['Close']]
print(price.info())
scaler = MinMaxScaler(feature_range = (-1, 1))
price['Close'] = scaler.fit_transform(price['Close'].values.reshape(-1, 1))

# Data Split
def data_split(stock, lookback):
  raw_data = stock.to_numpy()
  data = []

  for index in range(len(raw_data) - lookback):
    data.append(raw_data[index: index + lookback])
  data = np.array(data)
  test_size = int(np.round(0.2*data.shape[0]))
  train_size = data.shape[0] - test_size

  x_train = data[:train_size,:-1,:]
  y_train = data[:train_size,-1,:]
  x_test = data[train_size:,:-1,:]
  y_test = data[train_size:,-1,:]

  return [x_train, y_train, x_test, y_test]

window = 20 # choose sequence length
x_train, y_train, x_test, y_test = data_split(price, window)

print('x_train.shape = ',x_train.shape)
print('y_train.shape = ',y_train.shape)
print('x_test.shape = ',x_test.shape)
print('y_test.shape = ',y_test.shape)

# Transform into tensors
x_train = torch.from_numpy(x_train).type(torch.Tensor)
x_test = torch.from_numpy(x_test).type(torch.Tensor)
y_train = torch.from_numpy(y_train).type(torch.Tensor)
y_test = torch.from_numpy(y_test).type(torch.Tensor)
