FROM golang:1.20.5 AS build
WORKDIR /tmp
COPY app.go .
RUN GO111MODULE=off GOOS=linux go build -a -installsuffix cgo -o app . && chmod +x ./app

FROM gcr.io/distroless/base
WORKDIR /tmp
COPY --from=build /tmp/app .
CMD ["./app"]
