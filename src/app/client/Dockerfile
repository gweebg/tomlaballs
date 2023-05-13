FROM node:18 as build-step

# install dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

# Copy all local files into the image.
COPY . .

RUN npm run build

FROM nginx
COPY --from=build-step /app/dist /usr/share/nginx/html
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]