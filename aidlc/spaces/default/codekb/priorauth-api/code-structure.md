# Code structure
```
priorauth-api/
  pom.xml                                   Maven: parent spring-boot-starter-parent 4.1.1, two starters, boot plugin
  src/main/java/com/acmehealth/priorauth/
    PriorAuthApiApplication.java            entry point
    api/PendingRequestsController.java      GET /requests/pending
    api/PendingRequestResponse.java         the row the screen receives
    model/PriorAuthRequest.java             the domain record; isPending()
    store/RequestStore.java                 loads data/requests.sample.json, oldest first; pending()
  src/main/resources/application.yml        name, port
  src/main/resources/data/requests.sample.json
  src/test/java/com/acmehealth/priorauth/   RequestStoreTest (2), PendingRequestsControllerTest (1, @SpringBootTest + MockMvc)
```
