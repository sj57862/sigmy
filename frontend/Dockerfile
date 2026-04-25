FROM node:20

WORKDIR /app

COPY ang_sig/package*.json ./
RUN npm install

COPY ang_sig/ .

EXPOSE 4200

CMD ["npm", "start", "--", "--host", "0.0.0.0"]