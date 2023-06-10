FROM golang:1.20.5
WORKDIR /tmp
COPY app.go .
RUN GO111MODULE=off GOOS=linux go build -a -installsuffix cgo -o app .  && chmod +x ./app
CMD ["./app"]
