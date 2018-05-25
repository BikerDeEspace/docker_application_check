
FROM microsoft/aspnetcore-build:2.0
WORKDIR /app

ARG user1=someuser
# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN  --from=build-env dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c \ 
    Release -o out

RUN

# Build runtime image
FROM microsoft/aspnetcore:2.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "aspnet app.dll"]

EXPOSE 80
